---
title: CIP Experimental
---

This page provides user documentation for some experimental functions of the [CIP](/plugins/cip) package

{% include cip/nav %}

# **track**

<span style="font-size:110%">**Description**</span>  
This function allow to track the region defined in a list of label map image and return a measures table describing the tracks.

<span style="font-size:110%">**Signature**</span>  
    `measure, trackmate model = cip.track( inputImages*, radius*, gap frame, gap radius, split, merge, output )`  
     will track the regions in input images according to user provided parameter.

<span style="font-size:110%">**Input**</span>  
    **inputImages\*** : a list of label maps representing the regions to track. label maps should be organized in ascending time order  
    **radius\*** : a scalar representing the maximum distance, in pixel, at which to search the next region in the following frame.  
    **gap frame** : a scalar representing the maximum number of frame between 2 regions to be linked. This feature helps to track an objects that are not detected in some frame.  
    **gap radius** : a scalar representing the maximum distance, in pixel, at which to search the next region when closing a gap (i.e. if the region was not detected in some frames). This value could be larger than radius as the region is likely to be further away if not detected for a few frames.  
    **split** : a boolean value indicating whether or not to allow track splitting. Default is False. Set it to True if you want to detect some mitosis event for instance.  
    **merge** : a boolean value indicating whether or not to allow track merging. Default is False. Set it to True if you want to detect some vesicles fusion for instance.  
    **output** : a string in {'measure', 'trackmate', 'all'} determining how the tracking is returned. If value is set to 'measure' a [measure table](/plugins/cip/utilities#measure) is returned, if set to 'trackmate' a TrackmateModel object is returned.

<span style="font-size:110%">**Output**</span>  
    **measure**: a measure table providing all the necessary information to analyze and display the tracks. The measure rows provide spot position ordered by trackId, branchId (i.e. the sub branch of a track) and time. The branch graph for each track is defined by the parameter branchIn and branch out indicatin the branchId of the connected branch. The measure table can be visualized with cip.show  
    **trackmate model**: a TrackmateModel instance that can be further used for visualisation or saving the track information to disk. One can refer to [ trackmate scripting resource](/plugins/trackmate/scripting) for more information on how to use trackmate model. [cip.show](/plugins/cip/utilities#show) also provide some convenience to display result in trackschme or in image overlay.

<span style="font-size:110%">**Example**</span>  
one can find an example script [here](https://github.com/benoalo/CIP/blob/master/scripts/tracking_cip.py)

<span style="font-size:110%">**Implementation**</span>  
the track function detect the position of labelmap region at each time step load this information in trackmate\[1,2\] data structures before running the trackmate [tracking algorithm](https://github.com/fiji/plugins/trackmate/blob/master/src/main/java/fiji/plugin/trackmate/tracking/sparselap/SparseLAPTracker.java). the tracking

\[1\] Tinevez, J. Y., Perry, N., Schindelin, J., Hoopes, G. M., Reynolds, G. D., Laplantine, E., ... & Eliceiri, K. W. (2017). TrackMate: An open and extensible platform for single-particle tracking. Methods, 115, 80-90.

\[2\] [https://imagej.net/plugins/trackmate](https://imagej.net/plugins/trackmate)
