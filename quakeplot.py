"""
Earthquake Data Mining. CIS 210 W16 Project 9.2.
Author:  Joel Berry
Credits: Builds upon code in Bradley Miller & David Ranum, "Python  Programming in
Context", Second Edition, Ch. 4,7.

Access web data from USGS website, implement k-means cluster analysis
data mining algorithm to analyze and graphically report earthquake data.

User may change url in readeqf function as needed to plot different data sets.
See http://earthquake.usgs.gov/fdsnws/event/1/ for API to customize query.

Note: Cluster implementation currently separates geographically close events
east and west of the discontinuity at the +-180th meridian.
"""

import urllib.request
import math
import random
import turtle as t

def visualizeQuakes(k, r):
    """(int, int) -> None

    Top level function for accessing and analyzing earthquake data from USGS
    website.

    Calls readeqf, createCentroids, and createClusters, using parameter
    k number of clusters and r number of repetitions to run the k-means cluster
    analysis algorithm. Uses turtle module to graphically plot the M5 or
    greater earthquakes within the past month on a world map.
    Different queries can be plotted by altering the url in readeqf as per the
    USGS API. Color list currently permits only k values less than or equal
    to 30.

    Note 2: Map supplied in the original spec is a Mercator and plots
    incorrectly. Use the included Equirectangular Projection instead.

    Returns None.

    > visualizeQuakes(6, 50)
    <Draws Turtle Graphics map with 6 clusters.>
    """
    eq_dict = readeqf()
    centroids = createCentroids(k, eq_dict)
    clusters = createClusters(k, centroids, eq_dict, r)

    w = 1800 #Window width.
    h = 900 #Window height.
    bg_pic = "better_worldmap1800_900.gif"

    t.setup(width=w, height=h)
    t.bgpic(bg_pic)
    t.speed("fastest")
    t.hideturtle()
    t.up()

    w_factor = ((w / 2) / 180)
    h_factor = ((h / 2) / 90)

    color_list = ["dark red", "dark green", "dark blue", "dark orange",
                  "dark orchid", "dark goldenrod", "dark violet",
                  "pink", "magenta", "sky blue", "plum", "dark salmon",
                  "goldenrod", "chartreuse", "dark sea green", "cornsilk",
                  "dark olive green", "bisque", "blanched almond",
                  "dark cyan", "royal blue", "papaya whip", "peach puff",
                  "misty rose", "mint cream", "lavender blush", "hot pink",
                  "dark khaki", "cornflower blue", "chocolate"]

    for cluster_index in range(k):
        t.color(color_list[cluster_index])
        for akey in clusters[cluster_index]:
            lon = (eq_dict[akey][0]) * w_factor
            lat = (eq_dict[akey][1]) * h_factor
            t.goto(lon, lat)
            t.dot()
    return None


def createCentroids(k, data_dict):
    """(int, dict) -> list
    Accepts int value k, the number of desired centroids, and a dictionary with
    sequential integer keys starting at 1. Randomly selects keys and appends
    their values to list centroids.

    Note: Parameter k must be less than or equal to the length of data_dict.

    Returns centroids, the list of randomly chosen centroids.

    > createCentroids(2, {1: (1.0, -3.0), 2: (4.0, -6.5), 3: (-1.5, -9.3)})
    [(1.0, -3.0), (4.0, -6.5)] #Values are randomly selected.

    > createCentroids(2, {1: (1.0, -3.0), 2: (4.0, -6.5), 3: (-1.5, -9.3)})
    [(-1.5, -9.3), (1.0, -3.0)] #Values are randomly selected.
    """
    centroids = []
    centroid_count = 0
    centroid_keys = []
    while centroid_count < k:
        rkey = random.randint(1, len(data_dict))
        if rkey not in centroid_keys:
            centroids.append(data_dict[rkey])
            centroid_keys.append(rkey)
            centroid_count += 1
    return centroids

def createClusters(k, centroids, data_dict, repeats):
    """(int, list, dict, int) -> list

    K-means cluster analysis algorithm, accepts parameters:
    k, number of clusters; centroids, initial centroids;
    data_dict, data structure to analyze; and
    repeats, number of iterations to run the algorithm.

    Calls euclidD function.

    Note: Increasing number of repetitions generally increases accuracy of
    cluster grouping up to a point, with diminishing returns depending on size
    of data set, distribution, and number of clusters.

    Returns clusters, a list of lists of keys in data_dict representing clusters
    associated by Euclidean distance.

    > createClusters(3, <centroids>, <data_dict>, 20)
    [[1, 3, 12], [4, 7, 9, 10], [2, 5, 6, 8, 11]] # Results vary.

    """
    for i in range(repeats):
        clusters = []
        for i in range(k):
            clusters.append([])
        for akey in data_dict:
            distances = []
            for cluster_index in range(k):
                dist = euclidD(data_dict[akey], centroids[cluster_index])
                distances.append(dist)
            min_dist = min(distances)
            index = distances.index(min_dist)
            clusters[index].append(akey)
        for cluster_index in range(k):
            sums = [0] * len(data_dict[1]) #Number of dimensions.
            for akey in clusters[cluster_index]:
                data_points = data_dict[akey]
                for ind in range(len(data_points)):
                    sums[ind] += data_points[ind]
            for ind in range(len(sums)):
                cluster_len = len(clusters[cluster_index])
                if cluster_len != 0:
                    sums[ind] /= cluster_len
            centroids[cluster_index] = sums
    return clusters

def euclidD(pt_1, pt_2):
    """(list, list) -> float
    Accepts two lists of equal length, consisting of numeric values
    representing n-dimensional coordinates.

    Returns a float value, the Euclidean distance between the two points in
    n-dimensional space.

    >>> euclidD([0,0], [3,4])
    5.0
    >>> euclidD([-1,3,-6,2], [4,8,-1,7])
    10.0
    >>> euclidD([1,7], [6,-3])
    11.180339887498949
    """
    total = 0
    for i in range(len(pt_1)):
        diff = ((pt_1[i] - pt_2[i]) ** 2)
        total += diff
    return math.sqrt(total)

def readeqf():
    """() -> dict
    Accesses earthquake data from USGS website, storing latitude and
    longitude values in tuples of floats stored as dictionary values in eq_dict,
    with keys that are incrementing index integers starting at 1.

    Returns eq_dict.

    > readeqf() #Returned values are subject to change.
    {1: (148.88, -3.04), 2: (148.77, -3.28),..., 117: (-179.96, -30.76)}
    """
    #See http://earthquake.usgs.gov/fdsnws/event/1/ for API to change query.
    url = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=csv\
    &starttime=1956-01-01&minmagnitude=7"
    eq_dict = {}
    key = 0
    with urllib.request.urlopen(url) as webpage:
        webpage.readline() # Bypass header.
        for line in webpage:
            line = line.strip().decode("utf-8").split(",")
            key += 1
            eq_dict[key] = (round(float(line[2]), 2), round(float(line[1]), 2))
    return eq_dict


visualizeQuakes(10, 100)  #Test main function.
