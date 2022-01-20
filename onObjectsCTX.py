# Author:  Nikolai Makarov
# E-mail:  orgazmaat@gmail.com

# Tested on MAYA 2018.6
# run this from script editor or put on shelf
# can get UI window later with [createToolWindowUI()]


import maya.api.OpenMaya as api
import maya.api.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.cmds as mc

import math
import operator
import inspect


def inspectFile():
    """
    function returns name of file where it been used.
    Example used inside "HelloWorld_1.01.py" it will return
        "HelloWorld_1.01" as string
        "HelloWorld" as string
        "1.01" as string
        "%filePath%/HelloWorld_1.01" as string
    :return: file name (string), tool name , tool version (string), tool path

    usage:
        frame = inspect.stack()[1] #assigns "HelloWorld" to frame VAR
        versionName = inspect.stack()[2] #assigns "1.01" to versionName VAR
    #sacred
    """
    frame = inspect.stack()[1]
    fullFilePath = frame[0].f_code.co_filename
    filename = str('.').join((str(', ').join(fullFilePath.split("/")[-1:])).split("."))[:-3]
    return (str(', ').join(fullFilePath.split('/')[-1:]))[:-3], (str('').join(filename.split('_')[0])), (str(', ').join(fullFilePath.split('_')[-1:]))[:-3], fullFilePath

def stringToVector(stringVectorArg):
    """
    :param stringVectorArg: string representing a vector in format  (0.0, -1.0, 0.5)
    :return: NEW maya api vector (MVector)
    """
    stringToVectorize = ((stringVectorArg.replace("(", "")).replace(")", "")).split(",")
    returnVector=api.MVector(float(stringToVectorize[0]), float(stringToVectorize[1]), float(stringToVectorize[2]))
    return returnVector


# -----Hidden Parameters-----

ctx = 'putLocator'
intersectionParameter = 9999  # TODO add special optionVar for this parameter
isParallelTolerance = 1.0e-5  # TODO add special optionVar for this parameter
isEquivalentTolerance = 1.0e-5  # TODO add special optionVar for this parameter
surfaceOffsetDVAL = 0.0  # TODO add special optionVar for this parameter
useOnlyBlankMeshGeo = True # TODO add special optionVar for this parameter And Flag in settings

posXVector = "(1.0,0.0,0.0)"
posYVector = "(0.0,1.0,0.0)"
posZVector = "(0.0,0.0,1.0)"
negXVector = "(-1.0,0.0,0.0)"
negYVector = "(0.0,-1.0,0.0)"
negZVector = "(0.0,0.0,-1.0)"


def omToOm2Vector(vector):
    '''

    gets input vector in OLD maya api (maya.OpenMaya/om) and returns same vector in NEW maya api (maya.api.OpenMaya/om2) format

    :param vector: inputVector
    :return: vector: outputVector

    #sacred
    '''

    returnVector=api.MVector(vector.x,vector.y,vector.z)
    return returnVector

def getFlatten(listToFlat):

    """
    :param listToFlat: anything ,preferably list of strings
    :return: flatten list (list of strings)


    #sacred
    """

    preSelect=mc.ls(sl=True,fl=True)
    mc.select(cl=1)
    mc.select(listToFlat)
    flatten = mc.ls(sl=True, fl=True)
    mc.select(preSelect)
    return flatten

'''
# -----------------------NOTE-------------------------
# .upAxis method is not supported fully with current (2018.6) API version (maya.api.OpenMaya)
# https://forums.cgsociety.org/t/maya-2-0-api/1752925
# so we need to adapt it from OLD API using function above
# alternative method is to get "upAxisDirection" optionVar [mc.optionVar(q="upAxisDirection")]
'''

#those vectors here to set orientation for TOOL object
sceneUpVector = omToOm2Vector(om.MGlobal.upAxis())
secondaryUpVector = api.MVector(-1.0, 0.0, 0.0)

toolAimVector = api.MVector(1.0, 0.0, 0.0) #TOOL object AIM vector
toolUpVector = api.MVector(0.0, 1.0, 0.0) #TOOL object UP vector
toolOrientVector = api.MVector(1.0, 0.0, 0.0) #TOOL custom orient vector

def getMDagPath(node):
    selList = api.MSelectionList()
    selList.add(node)
    return selList.getDagPath(0)


#----UISettings----

# Colors
selectedItemsScroll = None
UIActiveState = [.45, .365, .0]
UIInactiveState = [.365, .365, .365]
bgcEdFalse = [0.170, 0.170, 0.170]
UIbgc = (0.265, 0.265, 0.265)

# UI buttons and columns
middleButtonWidth = 100
specialButtonWidth = 35
textWidth = 65

cwWidth = 295
cwHeight = 203
cwRows = [(1, 25), (2, textWidth), (3, 5), (4, middleButtonWidth), (5, 5), (6, specialButtonWidth), (7, 5)]
cwRowsOpt = [(1, 5), (2, 85), (3, 1), (4, 35), (5, 1), (6, 35), (7, 1), (8, 35), (9, 1), (10, 65), (11, 5)]
#########- WIP
cwRowsSlider = [(1, 5), (2, 85), (3, 1), (4, 115), (5, 1), (6, 65),(7,5)]


optionVarPrefix = "xz_"
optionVarFullPrefix = optionVarPrefix + inspectFile()[1] + "_"
toolWindowName = inspectFile()[1]

# ------- UI widgets -----------
# OVMARK  - add widget
widgetName1="addBaseMesh"
widgetName2="addToolMesh"
widgetName3="widgetName3"
widgetName4="widgetName4"
widgetName5="widgetName5"
widgetName6="widgetName6"
useTrueNormalWIG="useTrueNormalWIG"
useComponentNormalWIG="useComponentNormalWIG"
widgetName8="widgetName8"
widgetName9="widgetName9"
widgetName10="widgetName10"
widgetName11="widgetName11"
widgetName12="widgetName12"
widgetName13="widgetName13"
widgetName14="widgetName14"
widgetName15="widgetName15"
widgetName16="widgetName16"
widgetName17="widgetName17"
widgetName18="widgetName17"


widgetTool="widgetTool"
widgetBlank="widgetBlank"
upVectorWIGx="upVectorWIGx"
upVectorWIGy="upVectorWIGy"
upVectorWIGz="upVectorWIGz"

secondaryUpVectorWIGx="secondaryUpVectorWIGx"
secondaryUpVectorWIGy="secondaryUpVectorWIGy"
secondaryUpVectorWIGz="secondaryUpVectorWIGz"

toolAimVectorWIGx="toolAimVectorWIGx"
toolAimVectorWIGy="toolAimVectorWIGy"
toolAimVectorWIGz="toolAimVectorWIGz"

toolUpVectorWIGx="toolUpVectorWIGx"
toolUpVectorWIGy="toolUpVectorWIGy"
toolUpVectorWIGz="toolUpVectorWIGz"

toolOrientVectorWIGx="toolOrientVectorWIGx"
toolOrientVectorWIGy="toolOrientVectorWIGy"
toolOrientVectorWIGz="toolOrientVectorWIGz"



#TODO put all whose var stuff in MAIN


def doSomething(arg):
    # main action function - this structure helps to maintain similarity with other scripts and their UI windows
    if arg == "widgetName4":
        pass

    elif arg == widgetName11:
        # TODO insert ifwindowExist check - maybe i should feed BLANK and TOOL mehses names to OV

        if mc.window(toolWindowName, ex=True):
            getTool = mc.textField(widgetTool, q=True,text=1)
            getBlank = mc.textScrollList(widgetBlank, q=True, ai=True)
            # print(getBlank, getTool)
            if getTool and getBlank:
                ifContextToggle()
            else:
                print("------------ WARNING: TOOL or BLANK mehses invalid --------------------")
        else:
            mc.setToolTo("selectSuperContext")



    elif arg == widgetName1:
        refreshTextScrollUI(widgetBlank)

    elif arg == widgetName2:
        if len(mc.ls(sl=1, fl=True, type="transform")) > 0:
            mc.textField(widgetTool, tx=mc.ls(sl=1, fl=True, type="transform")[0], edit=True)
        else:
            print("------------ WARNING: Nothing selected -------------------")

    elif arg == widgetName3: #disabled in this version open "TOOL SETTINGS" in separate window
        # openOptionsWindow
        # onObjectOptions()
        pass

    elif arg == widgetName5:
        mc.optionVar(sv=(optionVarFullPrefix + "upVector", str(omToOm2Vector(om.MGlobal.upAxis()))))
        upVectorVAL = mc.optionVar(q=optionVarFullPrefix + "upVector")

        mc.floatField(upVectorWIGx, value=stringToVector(upVectorVAL).x, e=1)
        mc.floatField(upVectorWIGy, value=stringToVector(upVectorVAL).y, e=1)
        mc.floatField(upVectorWIGz, value=stringToVector(upVectorVAL).z, e=1)

    elif arg == widgetName6:
        mc.optionVar(sv=(optionVarFullPrefix + "secondaryUpVector", str(secondaryUpVector)))
        secondaryUpVectorVAL = mc.optionVar(q=optionVarFullPrefix + "secondaryUpVector")

        mc.floatField(secondaryUpVectorWIGx, value=stringToVector(secondaryUpVectorVAL).x, e=1)
        mc.floatField(secondaryUpVectorWIGy, value=stringToVector(secondaryUpVectorVAL).y, e=1)
        mc.floatField(secondaryUpVectorWIGz, value=stringToVector(secondaryUpVectorVAL).z, e=1)

################------Snap Functions---------------

def snapToEdge(arg1,arg2,arg3):
    """
    :param arg1: coords of POINT to project
    :param arg2: coords of START
    :param arg3: coords of END
    :return: resulting projection of POINT to line between START and END in form of vector
    """

    vector1 = arg3 - arg2
    vector2 = arg1 - arg2
    # returnCoord=coordPoint2-((coordPoint2-coordPoint1)/2)# edge middle
    returnCoord =arg2+vector1.normalize()*(vector1*vector2)    # point projection



    return returnCoord
#######################

def placeNormalNurbPoly(x,y,z):
    transformToPlace = str(mc.textField(widgetTool,q=True,text=1))
    # print("toolMesh:", transformToPlace)
    trueNormalNurbPoly= mc.duplicate(transformToPlace, rc=True, st=True)
    trueNormalNurbPolyPapa = trueNormalNurbPoly[0]
    mc.move(x, y, z, trueNormalNurbPolyPapa, absolute=True, rpr=True)
    mc.select(cl=1)

    return trueNormalNurbPoly

def orientToolTransform(objToRotate, vector1, vector2, vector3=None, vector4=None):
    """
    :param obj: object to orient dagPath (getMDagPath(node))
    :param vector1: aim vector
    :param vector2: up vector
    :param vector3: aimFace vector
    :param vector4: upFace vector
    :return:
    """
    # print
    ###---------------trying to set default UP vector------------

    if not vector3:  # this is made for easier orientation of object - it takes X-axis of object to aimed towards aimvector
        vector3 = api.MVector(1.0, 0.0, 0.0)

    if not vector4:  # this is made for easier orientation of object - it takes Y-axis of object to aimed towards aimvector
        vector4 = api.MVector(0.0, 1.0, 0.0)

    ###---------------normalize input vectors--------------------
    checkerU = vector1.normal()
    checkerV = vector2.normal()
    checkerAim = vector3.normal()
    checkerUp = vector4.normal()

    ### make sure vectors orthogonal to each over
    ### now we make sure that checkerV is orthogonal to both U and W by doing cross product again
    checkerW = (checkerU ^ checkerV).normal()  # crossproduct and normalize
    checkerV = (checkerW ^ checkerU).normal()

    quaternionCh = api.MQuaternion(checkerAim, checkerU)
    upRotatedCh = checkerUp.rotateBy(quaternionCh)


    # angleCh = math.acos(upRotatedCh.normal() * checkerV.normal())  # TODO returns math domain error if not normalized  - THIS ONE Still returns Math Domain Error
    ### dot product of 2 normalized vectors should return float(or scalar) between -1 and +1, but this not always work right - so simply clamp it
    angleCh = math.acos(max(min(upRotatedCh.normal() * checkerV.normal(), 1), -1))  # this one return no error made by SORT of CLAMPING:::max(min(my_value, max_value), min_value)


    quaternionVCh = api.MQuaternion(angleCh, checkerU)

    if not checkerV.isEquivalent(upRotatedCh.rotateBy(quaternionVCh), isEquivalentTolerance):
        angleCh = (2 * math.pi) - angleCh
        quaternionVCh = api.MQuaternion(angleCh, checkerU)

    quaternionCh *= quaternionVCh
    transformFnCh = api.MFnTransform(objToRotate)
    transformFnCh.setRotation(quaternionCh, api.MSpace.kWorld)




def initializeTool():
    if mc.window(toolWindowName, ex=True):
        mc.button(widgetName11, edit=1, dtg="Active", bgc=UIActiveState)

def finilizeTool():
    if mc.window(toolWindowName, ex=True):
        mc.button(widgetName11, edit=1, dtg="Inactive", bgc=UIInactiveState)

#############################
def mainPlaceFunc():
    # vpX, vpY, _ = mc.draggerContext(ctx, query=True, anchorPoint=True,snp=True)
    # pos = api.MPoint()
    # dir = api.MVector()
    # omui.M3dView().active3dView().viewToWorld(int(vpX), int(vpY), pos, dir)

    toolAimVector = stringToVector(mc.optionVar(q=optionVarFullPrefix + "toolAimVector"))
    toolUpVector = stringToVector(mc.optionVar(q=optionVarFullPrefix + "toolUpVector"))

    placementVector, orientVector, orientUpVector = mainPlaceFuncX()


    if placementVector:

        trueNormalNurbPoly=placeNormalNurbPoly(placementVector.x,placementVector.y, placementVector.z)
        objToManip = getMDagPath(trueNormalNurbPoly[0])
        orientToolTransform(objToManip, orientVector, orientUpVector, toolAimVector, toolUpVector)


    # return placementVector, orientVector, orientUpVector
##################################

def mainPlaceFuncX():
    vpX, vpY, _ = mc.draggerContext(ctx, query=True, anchorPoint=True,snp=True)
    pos = api.MPoint()
    dir = api.MVector()
    omui.M3dView().active3dView().viewToWorld(int(vpX), int(vpY), pos, dir)


    #return NONE of no intersections
    placementVector = None
    orientVector = None
    orientUpVector = None




    intersections={}  # declare a dictionary for intersections
    readOptionVars()


    #gather Initial Info from OV and UI fields
    if mc.window(toolWindowName, ex=True):
        baseMesh = mc.textScrollList(widgetBlank, q=True, ai=True)
    else:
        mc.setToolTo("selectSuperContext")
        baseMesh =None
        print(" ------------WARNING: TOOL or BLANK mehses invalid-------------------- ")


    # baseMesh = mc.textScrollList(widgetBlank, q=True, ai=True)
    useTrueNormal = mc.optionVar(q=optionVarFullPrefix + "useTrueNormal")

    sceneUpVector = stringToVector(mc.optionVar(q=optionVarFullPrefix + "upVector"))
    secondaryUpVector = stringToVector(mc.optionVar(q=optionVarFullPrefix + "secondaryUpVector"))

    # toolAimVector = stringToVector(mc.optionVar(q=optionVarFullPrefix + "toolAimVector"))
    # toolUpVector = stringToVector(mc.optionVar(q=optionVarFullPrefix + "toolUpVector"))

    surfaceOffset = mc.optionVar(q=optionVarFullPrefix + "surfaceOffset")

    #TODO make scheme easier to read by creating dictionary with all intersections

    # this scheme allows to return ONLY ONE intersection
    # in other case it will return closestIntersection for ALL shapes

    # # # ------------------ getting intersectionList ------------
    if baseMesh:
        for transformMesh in baseMesh:

            fnMesh = api.MFnMesh(getMDagPath(transformMesh))

            #TODO put check for transforms without transformMesh
            # childrenShape = mc.listRelatives(tran, c=True,type="mesh")
            # is it DONE ?

            childrenShape=mc.listRelatives(transformMesh,c=True,type="mesh") #get shape
            # print("childrenShape=", childrenShape)
            if childrenShape:
                intersection = fnMesh.closestIntersection(
                    api.MFloatPoint(pos), #returns list of 4 floats
                    api.MFloatVector(dir), #returns list of 3 floats
                    api.MSpace.kWorld,
                    # api.MSpace.kObject,
                    intersectionParameter,
                    False,
                    )

                if intersection[0] != api.MFloatPoint(0, 0, 0, 1):    # if it hits
                    hitPoint, hitRayParam, hitFace, hitTriangle, hitBary1, hitBary2 = intersection
                    x, y, z, _ = hitPoint


                    intersectionNormal = fnMesh.getClosestNormal(
                        api.MPoint(x, y, z),
                        api.MSpace.kWorld)
                        # api.MSpace.kObject)
                    returnMvector, returnInt  = intersectionNormal
                    nx, ny, nz = returnMvector

                    # trueNormal i don't like to mix with those ".f" things - reminds me old MEL
                    somestring, pInfX, pInfY, pInfZ = (mc.polyInfo(transformMesh + ".f[" + str(returnInt) + "]", fn=True))[0].split(":")[1].split(" ")
                    trueNormalVector = api.MVector(float(pInfX), float(pInfY), float(pInfZ))

                    #  shadingNormalVector
                    shadingNormalVector = api.MVector(float(nx), float(ny), float(nz))
                    intersections[transformMesh] = hitRayParam
                else:
                    print("------------ WARNING: No Intersections --------------------")

                # print("Intersections=", intersections)
            # print(transformMesh, "next transformMesh")

    # # # ------------------ if intersection exist : calculate closest one ------------
    if intersections:
        closestMeshTransform = min(intersections.iteritems(), key=operator.itemgetter(1))[0]  # this will always return SINGLE closestMeshTransform
        # print("closestMeshTransform=", closestMeshTransform)
        ###------------------ if closestMeshFound : put an object
        if closestMeshTransform:

            fnMesh = api.MFnMesh(getMDagPath(closestMeshTransform))

            intersection = fnMesh.closestIntersection(
                api.MFloatPoint(pos), #returns list of 4 floats
                api.MFloatVector(dir), #returns list of 3 floats
                api.MSpace.kWorld,
                intersectionParameter,
                False,
                )

            if intersection[0] != api.MFloatPoint(0, 0, 0, 1):    # if it hits
                hitPoint, hitRayParam, hitFace, hitTriangle, hitBary1, hitBary2 = intersection
                x, y, z, _ = hitPoint
                xHit, yHit, zHit, _ = hitPoint

                intersectionNormal = fnMesh.getClosestNormal(
                    api.MPoint(x, y, z),
                    api.MSpace.kWorld)

                returnMvector, returnInt  = intersectionNormal
                nx, ny, nz = returnMvector

                # trueNormal
                somestring, pInfX, pInfY, pInfZ = (mc.polyInfo(closestMeshTransform + ".f[" + str(returnInt) + "]", fn=True))[0].split(":")[1].split(" ")
                trueNormalVector = api.MVector(float(pInfX), float(pInfY), float(pInfZ))

                # shadingNormal
                shadingNormalVector = api.MVector(float(nx), float(ny), float(nz))

                #####################
                # trying to calculate closest vertex of mesh
                if mc.snapMode( q=True, point=True):   # if vertex snap is on
                    faceVerts = fnMesh.getPolygonVertices(hitFace)
                    faceVertsDistance = ((vertex, fnMesh.getPoint(vertex, api.MSpace.kWorld).distanceTo(api.MPoint(x, y, z)))
                                        for vertex in faceVerts)
                    closestVertexID , distanceTo = min(faceVertsDistance, key=operator.itemgetter(1))
                    print("-----------------Point SNAP CHECK---------") #
                    print("closestVertex:" ,closestVertexID , distanceTo )
                    # print(fnMesh.getPoint(closestVertex, api.MSpace.kWorld))
                    x, y, z , _ = fnMesh.getPoint(closestVertexID, api.MSpace.kWorld)

                if mc.snapMode(q=True, grid=True):  # if grid snap is on #TODO Component Normal
                    pass
                ###############################-----------------WIP
                if mc.snapMode(q=True, curve=True):  # if curve snap is on #TODO Component Normal
                    # fnMesh = api.MFnMesh(getMDagPath(closestMeshTransform))
                    faceVerts = fnMesh.getPolygonVertices(hitFace)
                    faceVertsDistance = ((vertex, fnMesh.getPoint(vertex, api.MSpace.kWorld).distanceTo(api.MPoint(x, y, z))) for vertex in faceVerts)
                    closestVertexID , distanceTo = min(faceVertsDistance, key=operator.itemgetter(1))
                    print("-----------------Edge SNAP CHECK---------") #


                    #DO NOT!!! calculate closest vertex

                    stringOfEdgeVerts = (mc.polyInfo(closestMeshTransform + ".vtx[" + str(closestVertexID) + "]", ve=True))[0].split(":")[1].split(" ")
                    stringOfEdgeIndexes = [elem for elem in stringOfEdgeVerts if elem][:-1]

                    # x, y, z, _ = fnMesh.getPoint(closestEdgePoint, api.MSpace.kWorld)
                    print("closestMeshTransform", closestMeshTransform)
                    print("stringOfEdgeIndexes", stringOfEdgeIndexes)  #
                    print("hitFace", hitFace)  #
                    # mc.polyListComponentConversion(closestMeshTransform +".f["+hitFace+"]", ff=True, te=True)



                    edgeNames =getFlatten( mc.polyListComponentConversion(closestMeshTransform +".f["+str(hitFace)+"]", ff=True, te=True))
                    print("edgeNames", edgeNames)
                    edgeIndex = [edgeName.split("[")[1].split("]")[0] for edgeName in edgeNames] #haha, got it
                    # print("edgeIndex", edgeIndex)  #


                    print("edgeIndex", edgeIndex ,"edgeIndexLen",len(edgeIndex))



                    #TODO this doesnt solve problem with concaveFaces

                    edgeIndex = set(edgeIndex)
                    stringOfEdgeIndexes =set(stringOfEdgeIndexes)
                    if useOnlyBlankMeshGeo:
                        stringOfEdgeIndexes = list(edgeIndex.intersection(stringOfEdgeIndexes))
                        print ("setIntersection",stringOfEdgeIndexes)
                    else:
                        stringOfEdgeIndexes = list(stringOfEdgeIndexes)
                    print("stringOfEdgeIndexes", stringOfEdgeIndexes)

                    ##########################
                    ##############################
                    ###############################


                    stringOfEdgeIndexes = set(edgeIndex) #this will iterate through all edges of hitface


                    projectionOnEdge = []
                    for edgeIndex in stringOfEdgeIndexes:
                        print (mc.xform(closestMeshTransform+".e["+edgeIndex+"]", q=1, t=1, ws=1))
                        edgeVertexCoords=mc.xform(closestMeshTransform + ".e[" + edgeIndex + "]", q=1, t=1, ws=1)
                        coordPoint1 = api.MVector(edgeVertexCoords[0],edgeVertexCoords[1],edgeVertexCoords[2])
                        coordPoint2 = api.MVector(edgeVertexCoords[3], edgeVertexCoords[4], edgeVertexCoords[5])
                        pointCoord = api.MVector(x,y,z)

                        # hitPointProjectionCoords = snapToEdge(pointCoord,coordPoint1,coordPoint2)
                        hitPointProjectionPoint = api.MPoint(snapToEdge(pointCoord, coordPoint1, coordPoint2))

                        #(coordPoint1 + coordPoint2)/2
                        print ("edgeCenter:",(coordPoint1 + coordPoint2)/2)
                        edgeCenterMVect = (coordPoint1 + coordPoint2) / 2
                        api.MPoint(edgeCenterMVect.x,edgeCenterMVect.y,edgeCenterMVect.z)
                        #find Center of EDGE
                        #find distance to one of vertex(radius)
                        #compare distance to hitPointProjectionPoint from Center of EDGE
                        #if distance is less then radius - append to list
                        # projectionOnEdge[edgeIndex] = hitPointProjectionPoint.distanceTo(api.MPoint(x, y, z))
                        # if hitPointProjectionPoint.distanceTo(api.MPoint(edgeCenterMVect.x,edgeCenterMVect.y,edgeCenterMVect.z))<= hitPointProjectionPoint.distanceTo(api.MPoint(coordPoint1.x,coordPoint1.y,coordPoint1.z)):
                        #     projectionOnEdge.append((edgeIndex, hitPointProjectionPoint.distanceTo(api.MPoint(x, y, z))))

                        projectionOnEdge.append((edgeIndex, hitPointProjectionPoint.distanceTo(api.MPoint(x, y, z))))

                    print(projectionOnEdge)
                    print(min(projectionOnEdge,key=operator.itemgetter(1)))
                    # closestEdgeIndex=(min(projectionOnEdge, key=operator.itemgetter(1)))[0]
                    # print((min(projectionOnEdge, key=operator.itemgetter(1)))[0])
                    closestEdgeIndex = (min(projectionOnEdge, key=operator.itemgetter(1)))[0]
                    print("closestEdgeIndex",closestEdgeIndex)
                    closestEdgeCoords=(mc.xform(closestMeshTransform + ".e[" + (min(projectionOnEdge, key=operator.itemgetter(1)))[0] + "]", q=1, t=1, ws=1))
                    coordPoint1 = api.MVector(closestEdgeCoords[0], closestEdgeCoords[1], closestEdgeCoords[2])
                    coordPoint2 = api.MVector(closestEdgeCoords[3], closestEdgeCoords[4], closestEdgeCoords[5])
                    pointCoord = api.MVector(x, y, z)

                    x, y, z, = snapToEdge(pointCoord, coordPoint1, coordPoint2)

                    #######################
                    #######################
                    #######################

                meshWM = api.MMatrix(mc.xform(closestMeshTransform, query=True, matrix=True, ws=True))

                # TODO chooseNORMAL to use
                # if ComponentNormal:
                    # if pointSnap ----> use closestVertexNormal
                    # if edgeSnap -----> use edgeCenterNormal
                    # if pointSnap AND edgeSnap ----> use edgeCenterNormal

                if useTrueNormal:
                    trueNormalVectorInMeshWM = trueNormalVector.transformAsNormal(meshWM)
                else:
                    # meshWM = api.MMatrix(mc.xform(transformMesh, query=True, matrix=True, os=True))
                    trueNormalVectorInMeshWM = shadingNormalVector

                #TODO CalculateUPVrctorRight

                calculateUpVector = sceneUpVector.transformAsNormal(meshWM)
                calculateUpVectorN = calculateUpVector.normalize()

                #############################
                # place curves - this made for diagnostic and debug
                # mc.curve(d=1, p=[(x, y, z), (x + trueNormalVectorInMeshWM.x, y + trueNormalVectorInMeshWM.y, z + trueNormalVectorInMeshWM.z)], k=[0, 1])
                # mc.curve(d=1, p=[(x, y, z), (x + calculateUpVectorN.x, y + calculateUpVectorN.y, z + calculateUpVectorN.z)], k=[0, 1])
                ##########################################

                #TODO put orient vectors selection here

                #############################
                #############################
                #############################

                if mc.snapMode(q=True, curve=True):  # if curve snap is on #TODO Component Normal ORIENTED WRONg

                    print(closestEdgeIndex,xHit,yHit,zHit)

                    if useComponentNormalVAL:


                        orientUpVector = coordPoint1 - coordPoint2
                        orientVector = trueNormalVectorInMeshWM

                        #MARK_ONE
                        # getFacesConnectedToEdge
                        #check if edge is valid ( only 2 face per edge )
                        # get Normals for faces
                        # calculate edgeNormal by summarizing face Normals and normalize it
                        # set orientVector to calculated edgeNormal



                        neighborFaceIndexes = mc.polyInfo( closestMeshTransform + ".e[" + str(closestEdgeIndex) + "]",ef=True)[0].split(":")[1].split()
                        if len(neighborFaceIndexes)>2:
                            print (" ------------WARNING: edge has more than 2 nighbor faces-------------------- ")
                            orientUpVector = coordPoint1 - coordPoint2
                            orientVector = trueNormalVectorInMeshWM
                        else:
                            somestring, faceOneNormalX, faceOneNormalY, faceOneNormalZ = (mc.polyInfo(closestMeshTransform + ".f[" + str(neighborFaceIndexes[0]) + "]", fn=True))[0].split(":")[1].split(" ")
                            faceOneNormal= api.MVector(float(faceOneNormalX), float(faceOneNormalY), float(faceOneNormalZ))
                            somestring, faceTwoNormalX, faceTwoNormalY, faceTwoNormalZ = (mc.polyInfo(closestMeshTransform + ".f[" + str(neighborFaceIndexes[1]) + "]", fn=True))[0].split(":")[1].split(" ")
                            faceTwoNormal = api.MVector(float(faceTwoNormalX), float(faceTwoNormalY), float(faceTwoNormalZ))

                            orientVector = (faceOneNormal+faceTwoNormal).normalize()
                            orientVector = orientVector.transformAsNormal(meshWM) # place it inWM



                            orientUpVector = coordPoint1 - coordPoint2

                            # trueNormalVectorInMeshWM = trueNormalVector.transformAsNormal(meshWM)


                        # filename = str('.').join((str(', ').join(fullFilePath.split("/")[-1:])).split("."))[:-3]

                        # somestring, pInfX, pInfY, pInfZ = (mc.polyInfo(closestMeshTransform + ".f[" + str(returnInt) + "]", fn=True))[0].split(":")[1].split(" ")
                        # trueNormalVector = api.MVector(float(pInfX), float(pInfY), float(pInfZ))





                    # orientVector = coordPoint2 - coordPoint1
                    # orientUpVector =(coordPoint2-pointCoord)^(coordPoint1-pointCoord).normal() #crossProduct

                    # orientUpVector = (coordPoint1-pointCoord) ^ (coordPoint2 - pointCoord).normal()  # crossProduct
                    # orientUpVector = (coordPoint1 - pointCoord.normal()) ^ (coordPoint2 - pointCoord) # crossProduct

                    # orientVector = (coordPoint2-pointCoord)^(coordPoint1-pointCoord).normal() #crossProduct
                    else:
                        orientVector = trueNormalVectorInMeshWM
                        orientUpVector = coordPoint1 - coordPoint2


                else:
                    orientVector = trueNormalVectorInMeshWM
                    orientUpVector = calculateUpVectorN
                #############################
                #############################
                #############################

                intersectionVector = api.MVector(x,y,z)
                if orientVector.isParallel(orientUpVector, isParallelTolerance):
                    print("----------- WARNING: Resulting normal and upVector are collinear -----------")
                    safeVector = secondaryUpVector # TODO putOV check here
                    meshWM = api.MMatrix(mc.xform(closestMeshTransform, query=True, matrix=True, ws=True))
                    orientUpVector = safeVector.transformAsNormal(meshWM)
                ############################################

                # place Tool transforms
                # TODO chooseSnapCoords to use
                # if ComponentNormal:
                    # if pointSnap ----> use closestVertexCoords
                    # if edgeSnap -----> use edgeCenterCoords
                    # if pointSnap AND edgeSnap ----> use closestVertexCoords
                    # if gridSnap ----> use closestVertexCoords

                # TODO put offset for placement
                placementVector = intersectionVector+(orientVector * surfaceOffset)

            else:
                # print("------------------- WARNING: No intersections -----------------")
                pass

            #TODO add functionality to randomly rotate placer transform around face normal
            if intersection[0] != api.MFloatPoint(0, 0, 0, 1):
                """
                x , y , z
                orientVector,
                orientUpVector, 
                toolAimVector,
                toolUpVector
                """

                # trueNormalNurbPoly=placeNormalNurbPoly(placementVector.x,placementVector.y, placementVector.z)
                # objToManip = getMDagPath(trueNormalNurbPoly[0])
                # orientToolTransform(objToManip, orientVector, orientUpVector, toolAimVector, toolUpVector) #TODO make sure its under OV coverage

                # return placementVector, orientVector, orientUpVector

    return placementVector, orientVector, orientUpVector

def ifContextToggle():
    currentCtx = mc.currentCtx()
    if mc.draggerContext(ctx, exists=True):
        mc.deleteUI(ctx)
    if currentCtx != ctx:
        mc.draggerContext(ctx, pressCommand=mainPlaceFunc, name=ctx, cursor='crossHair', fnz=finilizeTool, inz=initializeTool, snp=True)
        mc.setToolTo(ctx)
    else:
        mc.setToolTo("selectSuperContext")


'''
# -----------------------NOTE-------------------------
# Make class special for optionVars and UI widgets.
# Those set of functions are to complicated and workflow hard to understand
# -----------------------NOTE-------------------------
# readOptionVars()
# optionMenuChangeUI()
# updateOptionVars()
# performFlushToolOV()
# key code chunks marked as OVMARK
#
#
# wigName, wigOV, wigVAL ,wigDVAL - attributes to add in class
# putOV in updateOptionVars() 2 sections
# putOV in onObjectOptions() start section
'''


def readOptionVars():
    # OVMARK

    global secondaryUpVectorVAL
    global toolAimVectorVAL
    global toolUpVectorVAL
    global upVectorVAL
    global useTrueNormalVAL
    global useComponentNormalVAL
    global surfaceOffsetVAL
    global toolOrientVectorVAL
    # -------------------Initialize Option Vars----------------------
    # OVMARK
    if mc.optionVar(exists=optionVarFullPrefix + "useTrueNormal") == 0:
        useTrueNormalVAL = mc.optionVar(iv=(optionVarFullPrefix + "useTrueNormal", 1))
    useTrueNormalVAL = mc.optionVar(q=optionVarFullPrefix + "useTrueNormal")

    if mc.optionVar(exists=optionVarFullPrefix + "useComponentNormal") == 0:
        useComponentNormalVAL = mc.optionVar(iv=(optionVarFullPrefix + "useComponentNormal", 1))
    useComponentNormalVAL = mc.optionVar(q=optionVarFullPrefix + "useComponentNormal")

    if mc.optionVar(exists=optionVarFullPrefix + "upVector") == 0:
        upVectorVAL = mc.optionVar(sv=(optionVarFullPrefix + "upVector", str(omToOm2Vector(om.MGlobal.upAxis()))))
    upVectorVAL = mc.optionVar(q=optionVarFullPrefix + "upVector")

    if mc.optionVar(exists=optionVarFullPrefix + "secondaryUpVector") == 0:
        secondaryUpVectorVAL = mc.optionVar(sv=(optionVarFullPrefix + "secondaryUpVector", str(secondaryUpVector)))
    secondaryUpVectorVAL = mc.optionVar(q=optionVarFullPrefix + "secondaryUpVector")

    if mc.optionVar(exists=optionVarFullPrefix + "toolAimVector") == 0:
        toolAimVectorVAL = mc.optionVar(sv=(optionVarFullPrefix + "toolAimVector", str(toolAimVector)))
    toolAimVectorVAL = mc.optionVar(q=optionVarFullPrefix + "toolAimVector")

    if mc.optionVar(exists=optionVarFullPrefix + "toolUpVector") == 0:
        toolUpVectorVAL = mc.optionVar(sv=(optionVarFullPrefix + "toolUpVector", str(toolUpVector)))
    toolUpVectorVAL = mc.optionVar(q=optionVarFullPrefix + "toolUpVector")

    if mc.optionVar(exists=optionVarFullPrefix + "surfaceOffset") == 0:
        surfaceOffsetVAL = mc.optionVar(fv=(optionVarFullPrefix + "surfaceOffset", surfaceOffsetDVAL))
    surfaceOffsetVAL = mc.optionVar(q=optionVarFullPrefix + "surfaceOffset")

    if mc.optionVar(exists=optionVarFullPrefix + "toolOrientVector") == 0:
        toolOrientVectorVAL = mc.optionVar(sv=(optionVarFullPrefix + "toolOrientVector", str(toolOrientVector)))
    toolOrientVectorVAL = mc.optionVar(q=optionVarFullPrefix + "toolOrientVector")


def updateOptionVars():
    # OVMARK
    useTrueNormalVAL = mc.checkBox(useTrueNormalWIG, q=1, v=1)
    useComponentNormalVAL = mc.checkBox(useComponentNormalWIG, q=1, v=1)
    upVectorVAL = "(" + str(mc.floatField(upVectorWIGx,q=1,v=1)) + ", " + str(mc.floatField(upVectorWIGy,q=1,v=1)) + ", " + str(mc.floatField(upVectorWIGz,q=1,v=1)) + ")"
    secondaryUpVectorVAL ="("+str(mc.floatField(secondaryUpVectorWIGx,q=1,v=1))+", "+str(mc.floatField(secondaryUpVectorWIGy,q=1,v=1))+ ", "+str(mc.floatField(secondaryUpVectorWIGz,q=1,v=1))+")"
    toolAimVectorVAL = "(" + str(mc.floatField(toolAimVectorWIGx, q=1, v=1)) + ", " + str(mc.floatField(toolAimVectorWIGy, q=1, v=1)) + ", " + str(mc.floatField(toolAimVectorWIGz, q=1, v=1)) + ")"
    toolUpVectorVAL = "(" + str(mc.floatField(toolUpVectorWIGx, q=1, v=1)) + ", " + str(mc.floatField(toolUpVectorWIGy, q=1, v=1)) + ", " + str(mc.floatField(toolUpVectorWIGz, q=1, v=1)) + ")"

    surfaceOffsetVAL = mc.floatSliderGrp(widgetName15, q=1, v=1)

    # --------------------------------------------------------------------
    # OVMARK
    mc.optionVar(iv=(optionVarFullPrefix + "useTrueNormal", (useTrueNormalVAL)))
    mc.optionVar(iv=(optionVarFullPrefix + "useComponentNormal", (useComponentNormalVAL)))

    mc.optionVar(sv=(optionVarFullPrefix + "upVector", (upVectorVAL)))
    mc.optionVar(sv=(optionVarFullPrefix + "secondaryUpVector", (secondaryUpVectorVAL)))
    mc.optionVar(sv=(optionVarFullPrefix + "toolAimVector", (toolAimVectorVAL)))
    mc.optionVar(sv=(optionVarFullPrefix + "toolUpVector", (toolUpVectorVAL)))

    mc.optionVar(fv=(optionVarFullPrefix + "surfaceOffset", (surfaceOffsetVAL)))

def performFlushToolOV(arg):
    optionVarList = mc.optionVar(list=True)
    for OV in optionVarList:
        if arg in OV:
            mc.optionVar(rm=OV)




def refreshTextScrollUI(scrollListArg):
    listSelected = mc.ls(sl=1, fl=1,et="transform")
    if scrollListArg:
        mc.textScrollList(scrollListArg, e=True, ra=True)
        mc.textScrollList(scrollListArg, e=True, append=listSelected, ams=True)

def addSpecialButtonUI(toggleButtonName, commandString, symbol):
    if mc.optionVar(exists=optionVarFullPrefix + toggleButtonName) == 0:
        mc.optionVar(sv=(optionVarFullPrefix + toggleButtonName, "Inactive"))
    xz_optionVarVAL = mc.optionVar(q=optionVarFullPrefix + toggleButtonName)

    if xz_optionVarVAL == "Active":
        bgcState = UIActiveState
    else:
        bgcState = UIInactiveState

    mc.button(toggleButtonName, label=symbol, command=commandString + '("%s")' % toggleButtonName, dtg=xz_optionVarVAL, bgc=bgcState, width=specialButtonWidth, height=25, align='left')

def buttonStateToggleUI(widgetNameArg):
    q = mc.button(widgetNameArg, q=1, dtg=True)
    if mc.optionVar(exists=optionVarFullPrefix + widgetNameArg) == 0:
        mc.optionVar(sv=(optionVarFullPrefix + widgetNameArg, "Inactive"))
    if (q != "Active"):
        mc.button(widgetNameArg, edit=1, dtg="Active", bgc=UIActiveState)
        mc.optionVar(sv=(optionVarFullPrefix + widgetNameArg, "Active"))
        # print(mc.button(widgetNameArg, q=1, dtg=True))

    else:
        mc.button(widgetNameArg, edit=1, dtg="Inactive", bgc=UIInactiveState)
        mc.optionVar(sv=(optionVarFullPrefix + widgetNameArg, "Inactive"))

def buttonStateActivateUI(widgetNameArg):
    mc.button(widgetNameArg, edit=1, dtg="Active", bgc=UIActiveState)
    mc.optionVar(sv=(optionVarFullPrefix + widgetNameArg, "Active"))

def buttonStateDeactivateUI(widgetNameArg):
    mc.button(widgetNameArg, edit=1, dtg="Inactive", bgc=UIInactiveState)
    mc.optionVar(sv=(optionVarFullPrefix + widgetNameArg, "Inactive"))

def buttonStateToggleEchoUI(widgetNameArg):
    buttonStateToggleUI(widgetNameArg)
    print("doing other things",widgetNameArg)

def optionMenuChangeUI(widgetArg):
    checkMenuOption = (mc.optionMenuGrp(widgetArg, q=1, v=1))

    if checkMenuOption == " <-":
        pass
    else:
        if widgetArg == widgetName9:
            if checkMenuOption == "+X":
                toolAimVectorVAL = posXVector
            elif checkMenuOption == "+Y":
                toolAimVectorVAL = posYVector
            elif checkMenuOption == "+Z":
                toolAimVectorVAL = posZVector
            elif checkMenuOption == "-X":
                toolAimVectorVAL = negXVector
            elif checkMenuOption == "-Y":
                toolAimVectorVAL = negYVector
            elif checkMenuOption == "-Z":
                toolAimVectorVAL = negZVector

            mc.floatField(toolAimVectorWIGx, value=stringToVector(toolAimVectorVAL).x, e=1)
            mc.floatField(toolAimVectorWIGy, value=stringToVector(toolAimVectorVAL).y, e=1)
            mc.floatField(toolAimVectorWIGz, value=stringToVector(toolAimVectorVAL).z, e=1)

        if widgetArg == widgetName10:
            if checkMenuOption == "+X":
                toolUpVectorVAL = posXVector
            elif checkMenuOption == "+Y":
                toolUpVectorVAL = posYVector
            elif checkMenuOption == "+Z":
                toolUpVectorVAL = posZVector
            elif checkMenuOption == "-X":
                toolUpVectorVAL = negXVector
            elif checkMenuOption == "-Y":
                toolUpVectorVAL = negYVector
            elif checkMenuOption == "-Z":
                toolUpVectorVAL = negZVector

            mc.floatField(toolUpVectorWIGx, value=stringToVector(toolUpVectorVAL).x, e=1)
            mc.floatField(toolUpVectorWIGy, value=stringToVector(toolUpVectorVAL).y, e=1)
            mc.floatField(toolUpVectorWIGz, value=stringToVector(toolUpVectorVAL).z, e=1)

    updateOptionVars()

def createToolWindowUI():
    if mc.window(toolWindowName, ex=True):
        mc.deleteUI(toolWindowName)

    #-------------------Initialize Option Vars------------------------
    readOptionVars()

    currentWindow = mc.window(toolWindowName,width=cwWidth,height=cwHeight,rtf=1)

    mc.columnLayout(width=cwWidth)
    mc.frameLayout(label="Align to object Tool", collapsable=True, collapse=False,width=cwWidth-4)

    mc.rowLayout (numberOfColumns=3)

    mc.columnLayout()
    mc.rowColumnLayout(nc=7, cw=cwRows)
    mc.separator(height=10, style='none')

    mc.text(l='ToolMesh:', align="right")
    mc.separator(height=10, style='none')
    mc.textField(widgetTool, tx="", en=True, m=True, height=25, ed=False,bgc=bgcEdFalse , ann="ToolMesh")
    mc.separator(height=10, style='none')
    mc.button(widgetName2, label="<---", command='doSomething("%s")' % widgetName2, ann="Assign ToolMesh", width=specialButtonWidth, height=25, align='left')
    mc.separator(height=10, style='none')
    mc.setParent('..')


    mc.rowColumnLayout(nc=7, cw=cwRows)
    mc.separator(height=10, style='none')
    mc.text(l='BlankMesh:', align="right")

    mc.separator(height=10, style='none')
    mc.textScrollList(widgetBlank, h=100, en=False, ann="List of BlankMeshes")
    mc.separator(height=10, style='none')
    mc.button(widgetName1, label="<---", command='doSomething("%s")' % widgetName1, ann="Assign BlankMesh", width=specialButtonWidth, height=25, align='left')
    mc.separator(height=10, style='none')
    mc.setParent('..')

    mc.setParent('..')  # column

    mc.columnLayout()
    mc.separator(height=10, style='none')
    mc.button(widgetName11,label="InTool", command='doSomething("%s")' % widgetName11, ann="PlaceTool", width=specialButtonWidth, height=95, align='left')
    mc.separator(height=2, style='none')
    mc.button(widgetName3, label="", command='doSomething("%s")' % widgetName3, ann="Options", width=specialButtonWidth, height=30, align='left',en=0) # Settings Button - cut it
    mc.separator(height=10, style='none')
    mc.setParent('..')  # column

    mc.setParent('..')  #rowLayout
    mc.setParent('..')  #frameLayout

    mc.frameLayout("componentFrame", label="Align to component Tool", collapsable=True, collapse=True, width=cwWidth - 4)
    mc.setParent('..')  # frameLayout

    mc.frameLayout("settingsFrame",label="Settings", collapsable=True, collapse=True,width=cwWidth-4)

    mc.columnLayout(width=cwWidth)
    mc.separator(height=10, style='none')

    mc.rowLayout(nc=11, cw=cwRowsOpt, cat=(2, "right", 1))
    mc.separator(height=10, style='none')
    mc.text(l="UpVector:", ann=" UpVector", align="right")
    mc.separator(height=10, style='none')
    mc.floatField(upVectorWIGx, value=stringToVector(upVectorVAL).x, precision=1, ann=" Up Vector X ", cc="updateOptionVars()")
    mc.separator(height=10, style='none')
    mc.floatField(upVectorWIGy, value=stringToVector(upVectorVAL).y, precision=1, ann=" Up Vector Y ", cc="updateOptionVars()")
    mc.separator(height=10, style='none')
    mc.floatField(upVectorWIGz, value=stringToVector(upVectorVAL).z, precision=1, ann=" Up Vector Z ", cc="updateOptionVars()")
    mc.separator(height=10, style='none')
    mc.button(widgetName5, label="<-", bgc=UIInactiveState, ann=" Suggest Up Vector scene Up Axis", width=65, c="doSomething('%s')" % widgetName5)
    mc.separator(height=10, style='none')
    mc.setParent('..')

    mc.rowLayout(nc=11, cw=cwRowsOpt, cat=(2, "right", 1))
    mc.separator(height=10, style='none')
    mc.text(l="SafeVector:", ann="Secondary vector to orient ToolMesh, in case OrientNormal and UpVector are collinear ", align="right")
    mc.separator(height=10, style='none')
    mc.floatField(secondaryUpVectorWIGx, value=stringToVector(secondaryUpVectorVAL).x, precision=1, ann=" Safe Vector X ", cc="updateOptionVars()")
    mc.separator(height=10, style='none')
    mc.floatField(secondaryUpVectorWIGy, value=stringToVector(secondaryUpVectorVAL).y, precision=1, ann=" Safe Vector Y ", cc="updateOptionVars()")
    mc.separator(height=10, style='none')
    mc.floatField(secondaryUpVectorWIGz, value=stringToVector(secondaryUpVectorVAL).z, precision=1, ann=" Safe Vector Z ", cc="updateOptionVars()")
    mc.separator(height=10, style='none')
    mc.button(widgetName6, label="<-", bgc=UIInactiveState, ann=" Suggest Safe Vector -X ", width=65,c="doSomething('%s')" % widgetName6)
    mc.separator(height=10, style='none')
    mc.setParent('..')

    mc.separator(height=10, style='none')

    mc.rowLayout(nc=11, cw=cwRowsOpt, cat=(2, "right", 1))
    mc.separator(height=10, style='none')
    mc.text(l="ToolAimVector:", ann=" ToolAimVector", align="right")
    mc.separator(height=10, style='none')
    mc.floatField(toolAimVectorWIGx, value=stringToVector(toolAimVectorVAL).x, precision=1, ann=" Tool Aim Vector X ", cc="updateOptionVars()\nmc.optionMenuGrp('%s',e=1,v=' <-')" % widgetName9)
    mc.separator(height=10, style='none')
    mc.floatField(toolAimVectorWIGy, value=stringToVector(toolAimVectorVAL).y, precision=1, ann=" Tool Aim Vector Y ", cc="updateOptionVars()\nmc.optionMenuGrp('%s',e=1,v=' <-')" % widgetName9)
    mc.separator(height=10, style='none')
    mc.floatField(toolAimVectorWIGz, value=stringToVector(toolAimVectorVAL).z, precision=1, ann=" Tool Aim Vector Z ", cc="updateOptionVars()\nmc.optionMenuGrp('%s',e=1,v=' <-')" % widgetName9)
    mc.separator(height=10, style='none')

    # -----------------------
    mc.optionMenuGrp(widgetName9, cal=[1, "left"], cw1=10, width=65, cc='optionMenuChangeUI("%s")' % widgetName9)
    mc.menuItem(label=" <-", ann="use Custom Vector")
    mc.menuItem(label="+X", ann="use positive X preset")
    mc.menuItem(label="+Y", ann="use positive Y preset")
    mc.menuItem(label="+Z", ann="use positive Z preset")
    mc.menuItem(label="-X", ann="use negative X preset")
    mc.menuItem(label="-Y", ann="use negative Y preset")
    mc.menuItem(label="-Z", ann="use negative Z preset")

    mc.setParent('..', menu=True)
    mc.separator(height=10, style='none')
    mc.setParent('..')

    mc.rowLayout(nc=11, cw=cwRowsOpt, cat=(2, "right", 1))
    mc.separator(height=10, style='none')
    mc.text(l="ToolUpVector:", ann=" ToolUpVector ", align="right")
    mc.separator(height=10, style='none')
    mc.floatField(toolUpVectorWIGx, value=stringToVector(toolUpVectorVAL).x, precision=1, ann=" Tool Up Vector X ", cc="updateOptionVars()\nmc.optionMenuGrp('%s',e=1,v=' <-')" % widgetName10)
    mc.separator(height=10, style='none')
    mc.floatField(toolUpVectorWIGy, value=stringToVector(toolUpVectorVAL).y, precision=1, ann=" Tool Up Vector Y ", cc="updateOptionVars()\nmc.optionMenuGrp('%s',e=1,v=' <-')" % widgetName10)
    mc.separator(height=10, style='none')
    mc.floatField(toolUpVectorWIGz, value=stringToVector(toolUpVectorVAL).z, precision=1, ann=" Tool Up Vector Z ", cc="updateOptionVars()\nmc.optionMenuGrp('%s',e=1,v=' <-')" % widgetName10)
    mc.separator(height=10, style='none')

    mc.optionMenuGrp(widgetName10, cal=[1, "left"], cw1=10, width=65, cc='optionMenuChangeUI("%s")' % widgetName10)
    mc.menuItem(label=" <-", ann="use Custom Vector")
    mc.menuItem(label="+X", ann="use positive X preset")
    mc.menuItem(label="+Y", ann="use positive Y preset")
    mc.menuItem(label="+Z", ann="use positive Z preset")
    mc.menuItem(label="-X", ann="use negative X preset")
    mc.menuItem(label="-Y", ann="use negative Y preset")
    mc.menuItem(label="-Z", ann="use negative Z preset")

    mc.separator(height=10, style='none')
    mc.setParent('..')
#---------------------------------------ToolOrient
    # mc.separator(height=10, style='none')
    # mc.rowLayout(nc=11, cw=cwRowsOpt, cat=(2, "right", 1))
    # mc.separator(height=10, style='none')
    # mc.text(l="OrientVector:", ann=" OrientVector ", align="right")
    # mc.separator(height=10, style='none')
    # mc.floatField(toolOrientVectorWIGx, value=stringToVector(toolOrientVectorVAL).x, precision=1, ann=" Orient Vector X ", cc="updateOptionVars()\nmc.optionMenuGrp('%s',e=1,v=' <-')" % widgetName17)
    # mc.separator(height=10, style='none')
    # mc.floatField(toolOrientVectorWIGy, value=stringToVector(toolOrientVectorVAL).y, precision=1, ann=" Orient Vector Y ", cc="updateOptionVars()\nmc.optionMenuGrp('%s',e=1,v=' <-')" % widgetName17)
    # mc.separator(height=10, style='none')
    # mc.floatField(toolOrientVectorWIGz, value=stringToVector(toolOrientVectorVAL).z, precision=1, ann=" Orient Vector Z ", cc="updateOptionVars()\nmc.optionMenuGrp('%s',e=1,v=' <-')" % widgetName17)
    # mc.separator(height=10, style='none')
    #
    # mc.optionMenuGrp(widgetName18, cal=[1, "left"], cw1=10, width=65, cc='optionMenuChangeUI("%s")' % widgetName18)
    #
    # mc.menuItem(label=" 0", ann="use geo normal")
    # mc.menuItem(label=" 1", ann="use shading normal")
    # mc.menuItem(label=" 2", ann="use component normal then SNAP enabled")
    # mc.menuItem(label=" 3", ann="do not orient")
    # mc.menuItem(label=" <-", ann="use custom vector")
    #
    # mc.separator(height=10, style='none')
    # mc.setParent('..')
#-------------------------------

    mc.setParent('..')

    #########- WIP
    mc.columnLayout()
    mc.rowLayout(nc=7, cw=cwRowsSlider, cat=(2, "right", 1))
    mc.separator(height=10, style='none')
    mc.text(l="Offset:",ann=" Surface Offset", align="right")
    mc.separator(height=10, style='none')
    #TODO add adaptive scale for offset
    mc.floatSliderGrp(widgetName15, cw2=[35,75],pre=2, field=True, minValue=-1.0, maxValue=1.0, fieldMinValue=-10.0, fieldMaxValue=10.0, v=surfaceOffsetVAL ,ann=" Surface Offset", cc="updateOptionVars()")

    # mc.floatField(widgetName15, value=0, precision=1, ann=" Surface Offset", cc="updateOptionVars()")
    mc.separator(height=10, style='none')
    mc.button(widgetName16,label="<-", bgc=UIInactiveState, ann=" Suggest SurfaceOffset equal to ZERO", width=65, c="mc.floatSliderGrp('%s',e=1,v=0)\nupdateOptionVars()" % widgetName15)
    # mc.floatSlider(min=-100, max=100, value=0, step=1)

    mc.separator(height=10, style='none')
    mc.setParent('..')

    mc.separator(height=10, style='none')

    mc.rowLayout(nc=11, cw=cwRowsOpt, cat=[(2, "right", 1), (8, "right", 1)])  # useTrueNormal row
    mc.separator(height=10, style='none')
    mc.text(l="UseTrueNrml:", align="right", ann="use geometric normal - will use shading normal if unchecked")
    mc.separator(height=10, style='none')
    mc.checkBox(useTrueNormalWIG, label="", v=useTrueNormalVAL, cc="updateOptionVars()")

    mc.separator(height=10, style='none')
    mc.separator(height=10, style='none')
    mc.separator(height=10, style='none')
    mc.text(l="fOV:", align="right")
    mc.separator(height=10, style='none')
    mc.button(widgetName8, label="[X]", bgc=UIInactiveState, ann="removes OptionVars created by this TOOL ", c="performFlushToolOV('%s')" % optionVarFullPrefix, width=65)
    mc.separator(height=10, style='none')
    mc.setParent('..')

    mc.rowLayout(nc=11, cw=cwRowsOpt, cat=[(2, "right", 1), (8, "right", 1)])  # useTrueNormal row
    mc.separator(height=10, style='none')
    mc.text(l="UseCompNrml:", align="right",ann="use component normal then point snap is ON", vis=1) #TODO Component Normal
    mc.separator(height=10, style='none')

    mc.checkBox(useComponentNormalWIG, label="", v=useComponentNormalVAL, cc="updateOptionVars()", vis=1) #TODO Component Normal
    mc.separator(height=10, style='none')
    mc.setParent('..')

    mc.rowColumnLayout(nc=2, cw=[(1, 240), (2, 40)])
    mc.text(l='Version:', h=25, align="right")
    # mc.text(l=inspectFile()[2], h=25, align="right", ann="Version number")
    mc.text(l="1.00", h=25, align="right", ann="Version number")
    mc.setParent('..')

    mc.setParent('..')
    mc.showWindow(currentWindow)


# # draw window
# if mc.window(toolWindowName, ex=True):
#     mc.deleteUI(toolWindowName)
print(toolWindowName,inspectFile()[-2])
createToolWindowUI()

