import os, sys
import json

def python_packing(package, headless=False):
    if not headless:
        os.system(f"pipreqs { package['path'] } --force") # Overwrites existing requirements.txt
        os.system(f"pip install -r { package['path'] }/requirements.txt -t { package['path'] }")
        os.system(f"zip -r { package['path'] }--v{package['S3']['version']}.zip { package['path'] }")
    return f"{ package['path'] }--v{package['S3']['version']}.zip" # Package location with S3 version

# Strategy for packing resources for deployment, by language
packing_strategy = {
    'Python' : python_packing,
}

def main():
    output_commands = []
    # Get the branch name of the active GitHub repository
    branch = sys.argv[2].split('/')[-1]

    # Check if the resource manifest has been modified since the last time this script was run
    # If not then exit with error
    resource_change = 'house-keeping/resource-manifest.json' in sys.argv[1]
    if not resource_change:
        print('\n\nNo Resource Changes - Exiting\n\n')
        sys.exit(1)
    # Read in the resource manifest
    manifest = json.load(open('house-keeping/resource-manifest.json', 'r'))
    bucket_name_root = manifest['Config']['S3']['bucket-name-root']

    # Get S3 bucket name for the active GitHub repository and the contents of that bucket
    try:
        # CAVEAT : Will not error if the S3 bucket does not exist, will return same as empty bucket
        cmd = f"aws s3api list-objects --bucket {bucket_name_root}-{branch} --output json > gantry.json"
        os.system(cmd)
        output_commands.append(cmd)
        s3_bucket_ls = json.load(open('gantry.json'))['Contents']
    except:
        s3_bucket_ls = []
        
    # Identify AWS resource types that need to be packaged for deployment (lambdas, API Gateway, etc.)
    aws_resources = list(manifest.keys())
    for rsc in aws_resources: 
        # If the resource nodes needs to be packaged for deployment, then pack it
        if manifest[rsc]['build_to_deploy']:
            for num,resource in enumerate(manifest[rsc]['resources']):
                # Produce the filepath for the resource
                packed_key = packing_strategy[resource['language']['name']](resource,True)
                # If the packed resource version is in S3 already, then ignore it, otherwise add it to S3
                if packed_key not in list(map(lambda x: x['Key'], s3_bucket_ls)):
                    packing_strategy[resource['language']['name']](resource)
                    cmd = f"aws s3api put-object --bucket {bucket_name_root}-{branch} --key {packed_key.replace('./','')} --body {packed_key.replace('./','')}"
                    os.system(cmd)
                    output_commands.append(cmd)
    # Return the commands that were run
    return '\n'.join(output_commands)



if __name__ == "__main__":
    print(main())