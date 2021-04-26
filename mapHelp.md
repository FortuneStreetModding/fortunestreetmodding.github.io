---
title: HowTo upload Maps
layout: default
---
# How to upload a new map

To upload a new map to this repository you must create a pull request using the branch `master` as base. The pull request must contain the new folder for your map. The folder must contain:
- 1 .yaml file
- 1-4 .frb files
- at least one screenshot

You can take a look at one of the map templates [TemplateMap_Colony](../../tree/master/TemplateMap_Colony) or [TemplateMap_Colossus](../../tree/master/TemplateMap_Colossus) or the other maps in this repository.

**Please test your map at least one full game before creating a pull request!**

## Step by step guide

1. [Download](../../archive/master.zip) the repository to your computer and extract it to `C:\CommunityMaps-master`.

2. Create a new folder in `C:\CommunityMaps-master` and name it like your map, e.g. `C:\CommunityMaps-master\SuitsMap`. 

3. Prepare your map folder. Take a look into one of the map templates [TemplateMap_Colony](../../tree/master/TemplateMap_Colony) or [TemplateMap_Colossus](../../tree/master/TemplateMap_Colossus) how your map folder must look like.
![01_MapTemplate](01_MapTemplate.png)
The folder must contain:
- 1 .md file
- 1-4 .frb files
- at least one screenshot

4. Back at the [Community Maps repository](../../), click on the Fork button to create your personal fork.
![02_Fork](02_Fork.png)

5. Drag'n'drop your map folder into your forked repository.
![03_DragNDropFolder](03_DragNDropFolder.png)

6. Select `Create a new branch for this commit and start pull request`. Give the branch the same name as your map.
![04_NameBranchAndStartPullRequest](04_NameBranchAndStartPullRequest.png)

7. Click on `compare across forks`.
![05_CompareAcrossForks](05_CompareAcrossForks.png)

8. Select base repository `FortuneStreetModding/CommunityMaps`.
![06_SelectFortuneStreetCommunityMaps](06_SelectFortuneStreetCommunityMaps.png)

9. Make sure the base is set to `master`. You can now create the pull request.
![07_PullRequestReady](07_PullRequestReady.png)
