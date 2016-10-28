from shapely.geometry import  Point, LineString, LinearRing, Polygon, MultiPolygon

def toPolygon(polylines) :
    polygons = []
    for polyline in polylines :
        polygons.append(toSimplePolygon(polyline))

    nPolygons = [polygons[0]]
    for index in range(len(polygons)) :
        if index == 0 :
            continue
        c = polygons[index]
        nPolygons = compareAndReturn(nPolygons, c)
    if len(nPolygons) == 1 :
        return nPolygons[0]
    else :
        return MultiPolygon(nPolygons)


def compareAndReturn(polygons, c) :
    state = 'no_cross'
    contains = []
    for index in range(len(polygons)):
        polygon = polygons[index]
        if len(polygon.interiors) == 0 :
            if polygon.contains(c) :
                polygons[index] = Polygon(polygon.exterior, [c.exterior])
                return polygons
            elif c.contains(polygon) :
                state = 'c_contains'
                contains.append(index)
        else :
            if polygon.contains(c) :
                rings = []
                for interior in polygon.interiors :
                    rings.append(interior)
                rings.append(c.exterior)
                polygons[index] = Polygon(polygon.exterior, rings)
                return polygons

    if state == 'no_cross' :
        polygons.append(c)
    else :
        rings = []
        for index in contains :
            rings.append(polygons[index].exterior)

        polygons.append(Polygon(c.exterior, rings))
        time = 0
        for index in contains :
            del polygons[index - time]
            time = time + 1

    return polygons;

def toSimplePolygon(polyline) :
    points = [];
    lngLats = polyline.split(';')
    for lngLat in lngLats :
        point = lngLat.split(',')
        points.append(Point(float(point[0]), float(point[1])))
    ring = LinearRing(LineString(points));
    polygon = Polygon(ring)

    return polygon;
