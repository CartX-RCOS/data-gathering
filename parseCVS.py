import json

all_possible_endings = ["ct", "CT", "oz", "OZ", "mg", "MG"]

def parseCVS(data):
    ret = dict()
    name_list = data["name"].split("-")
    name = ""

    j = 0
    for i in range(0, len(name_list)):
        if name_list[i].isdigit() and name_list[i+1] not in all_possible_endings:
            break
        name += name_list[i] + " "
        j += 1

    ret["Name"] = name.strip()
    nums = name_list[j:]
    # print(nums)
    if nums:
        if len(nums) >= 3:
            size = '.'.join(nums[:2])
            ret["Size"] = size
        else:
            size = nums[0]
            ret["Size"] = size
        size_type = nums[-1]
        ret["Size Type"] = size_type
    return ret

with open('cvs.json', 'r') as file:
    data = json.load(file)

for item in data:
    ret = parseCVS(item)
    print(ret)