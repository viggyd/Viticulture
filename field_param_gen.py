from viticulture import FieldType
import json

def GenerateName(Fields):

    return "S{0:d}{1:d}_M{2:d}{3:d}_L{4:d}{5:d}_param.json".format(
        Fields[FieldType.SMALL]["Capacity"],
        Fields[FieldType.SMALL]["Layout"],
        Fields[FieldType.MEDIUM]["Capacity"],
        Fields[FieldType.MEDIUM]["Layout"],
        Fields[FieldType.LARGE]["Capacity"],
        Fields[FieldType.LARGE]["Layout"])


if __name__ == '__main__':


    Fields = {
        FieldType.SMALL : {"Capacity" : 0, "Layout" : 0},
        FieldType.MEDIUM : {"Capacity" : 6, "Layout" : 0},
        FieldType.LARGE : {"Capacity" : 7, "Layout" : 0}
    }


    # Medium field capacity is 6
    for i in range(7):
        Fields[FieldType.MEDIUM]["Layout"] = 2 * i - 6

        for j in range(8):
            Fields[FieldType.LARGE]["Layout"] = 2 * j - 7

            Name = GenerateName(Fields)


            with open(Name, 'w') as f:
                f.write(json.dumps(Fields))



