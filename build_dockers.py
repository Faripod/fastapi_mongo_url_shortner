import os

DOCKERS_FILE = (
    {
        'image_name': 'campaign_radar_cronjob_adform',
        'file_path': 'app/cronjob/adform/Dockerfile'
    },
    {
        'image_name': 'campaign_radar_cronjob_admanager',
        'file_path': 'app/cronjob/admanager/Dockerfile'
    },
    {
        'image_name': 'campaign_radar_cronjob_campaignmanager',
        'file_path': 'app/cronjob/campaignmanager/Dockerfile'
    },
    {
        'image_name': 'campaign_radar_cronjob_celtra',
        'file_path': 'app/cronjob/celtra/Dockerfile'
    },
    {
        'image_name': 'campaign_radar_cronjob_displayvideo',
        'file_path': 'app/cronjob/displayvideo/Dockerfile'
    },
    {
        'image_name': 'campaign_radar_cronjob_pushnotification',
        'file_path': 'app/cronjob/pushnotification/Dockerfile'
    },
    {
        'image_name': 'campaign_radar_cronjob_process_data',
        'file_path': 'app/cronjob/process_data/Dockerfile'
    },
)

# Login aws
os.system('aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 598573801421.dkr.ecr.eu-west-1.amazonaws.com')

for dk in DOCKERS_FILE:
    # Build dell'immagine
    os.system(f'docker build --platform linux/amd64 -t {dk["image_name"]} -f {dk["file_path"]} .')
    # Tag dell'immagine
    os.system(f'docker tag {dk["image_name"]}:latest 598573801421.dkr.ecr.eu-west-1.amazonaws.com/{dk["image_name"]}:latest')
    # Push dell'immagine
    os.system(f'docker push 598573801421.dkr.ecr.eu-west-1.amazonaws.com/{dk["image_name"]}:latest')