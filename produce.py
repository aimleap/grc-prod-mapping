import pandas as pd
import re
from datetime import datetime

def selectCategories(combinedDf):
    categoryList = """Fresh Fruits & Vegetables
    Fresh Produce
    Fruits & Vegetables
    Produce
    Grocery
    Natural & Organic
    Organic Shop""".split("\n")
    catDictList = []
    for category in categoryList:
        sub_categoryList = combinedDf[combinedDf['category']==category]['sub_category'].unique()
        print("category :",category)
        print(sub_categoryList)
        for subCate in sub_categoryList:
            cateDict = {}
            cateDict['category'] = category
            cateDict['subCate'] = subCate
            catDictList.append(cateDict)
        print("********************")
    cateDF = pd.DataFrame(catDictList)
    subCateList = """Dressings & Dips
    Salad
    Fresh Juice & Smoothies
    Dried Fruit & Nuts
    Party Trays
    Tofu/Soy Products
    Plant Based Protein & Tofu
    Fresh Packaged Salads, Dressings & Dips
    Nuts & Dried Fruits
    Fresh Juices
    Fresh Dressings & Dips
    Food Gifts
    Bakery & Bread
    Dairy & Eggs
    Grocery
    Frozen
    Spices & Baking
    Meat & Seafood
    Beverages
    Baby
    Bakery & Bread
    Cleaning & Household
    Beauty & Personal Care
    Deli
    Organic Beverages""".split("\n")
    cateDFFinal = pd.DataFrame()
    for subCate in subCateList:
        cateDF = cateDF[cateDF['subCate']!=subCate]
    cateDF = cateDF.reset_index(drop=True)
    newDf = pd.DataFrame()
    for row in cateDF[:].iterrows():
        row = row[1]
        category = row['category']
        subcategory = row['subCate']
        newDf = newDf.append(combinedDf[(combinedDf['category']==category) & (combinedDf['sub_category']==subcategory)])
    return newDf


def getStoreBrand(storeBrandList,title,organiclist):
    temptitle = title.replace("Simple Truth Organic","")
    storeBrand = [brand for brand in storeBrandList if brand in temptitle]
    print(organiclist)
    organic_ = [brand for brand in organiclist if brand in title]
    if len(storeBrand)!=0:
        status = "store brand"
    elif len(organic_)!=0:
        status = "organic"
    else:
        status = "national brand"

    return status

def extract_weight_count(product):

    weight = ""
    count = ""
     # Match weight with optional space and decimal support
#     weight_match = re.search(r'(\d+(\.\d+)?)\s?oz', product, re.IGNORECASE)
    weight_match = re.search(r'(\d+(\.\d+)?)\s?(oz|lb|lbs)', product, re.IGNORECASE)

    # Match count with optional space and variations of 'ct', 'Count', and 'Each'
    count_match = re.search(r'(\d+)?\s?(Count|ct|Each|each)', product, re.IGNORECASE)

    if weight_match:
        weight = weight_match.group(0).strip()

    if count_match:
        count_num = count_match.group(1)
        if count_num:
            count = count_num.strip() + ' Count'
        else:
            count = '1 Each'

    return weight, count
def getStoreBrand(storeBrandList,title,organiclist):
    temptitle = title.replace("Simple Truth Organic","")
    storeBrand = [brand for brand in storeBrandList if brand in temptitle]
    organic_ = [brand for brand in organiclist if brand in title]
    if len(storeBrand)!=0:
        status = "store brand"
    elif len(organic_)!=0:
        status = "organic"
    else:
        status = "national brand"

    return status
def cleanWeights(weight):
    weight = weight.lower().replace(" ",'').replace("ct",'count').replace("ounce",'oz')
    return weight

def getAvailableString(cateList,testString):
    availableCat2 = [i for i in cateList if i.lower().strip() in testString.lower().strip()]
    multipleSpacesList = [i for i in availableCat2 if len(i.split(" "))!=1]
    newList = []
    for spacesInCha in  multipleSpacesList:
        singleLetterAvailableList = [i for i in spacesInCha.split(" ") if i in availableCat2]
        [availableCat2.remove(i) for i in singleLetterAvailableList if i in availableCat2]
    #########################
    ExactMatchavailableCat2 = []
    singleLetterAvailableList = [i for i in availableCat2 if len(i.split(" ")) == 1]
    singleLetterAvailableList
    for test in singleLetterAvailableList:
        [ExactMatchavailableCat2.append(i) for i in testString.split(" ") if i==test]
    [availableCat2.remove(i) for i in singleLetterAvailableList if i not in ExactMatchavailableCat2]
    return " ".join(availableCat2)

def getAimleapTitle(testString):
    testString = testString.lower().replace(","," ").replace("!",' ').replace("("," ").replace(")",' ').replace("."," ").replace('"',' ').strip()

    if "potatoes" in testString:
        testString = testString.replace("potatoes","potato")
    if "tomatoes" in testString:
        testString = testString.replace("tomatoes","tomato")
    if "strawberries" in testString:
        testString = testString.replace("strawberries","strawberry")
    if "oinions" in testString:
        testString = testString.replace("oinions","onions")

    cate1 = getAvailableString(cate1List,testString)
    cate2 = getAvailableString(cate2List,testString)
    cate3 = getAvailableString(cate3List,testString)
    cate4 = getAvailableString(cate4List,testString)
    form1 = getAvailableString(forms,testString)

    label1_ = getAvailableString(labels1,testString)

    label2_ = getAvailableString(labels2,testString)
    with_ = getAvailableString(withList,testString)
    pack = getAvailableString(PackList,testString)

    aimleapTitleList = []
    aimleapTitleList.append(cate1)
    if cate2 not in aimleapTitleList:
        aimleapTitleList.append(cate2)
    if cate3 not in aimleapTitleList:
        aimleapTitleList.append(cate3)
    if cate4 not in aimleapTitleList:
        aimleapTitleList.append(cate4)
    if form1 not in aimleapTitleList:
        aimleapTitleList.append(form1)

    if label1_ not in aimleapTitleList:
        aimleapTitleList.append(label1_)
    if label1_ not in aimleapTitleList:
        aimleapTitleList.append(label2_)
    if with_ not in aimleapTitleList:
        aimleapTitleList.append(with_)

    aimleapTitle = " ".join([i for i in aimleapTitleList if i!=''])
    newTitle = []
    [newTitle.append(i) for i in aimleapTitle.lower().split(" ") if i not in newTitle]
    if "-" in newTitle:
        newTitle.remove("-")
    if "&" in newTitle:
        newTitle.remove("&")
    if "and" in newTitle:
        newTitle.remove("and")
    if "each" in newTitle:
        newTitle.remove("each")

    if "with" in newTitle:
        newTitle.remove("with")
    newTitle.sort()
    newTitle_ = removeLastSFromTitle(newTitle)
    return newTitle_

def cleanTitle(testStr):
    newtestStr = getNewStr(testStr)
    if "1 Each" in newtestStr:
        newtestStr = newtestStr.replace(" 1 Each",'').strip()+" 1 Each"
    return newtestStr

def getNewStr(testStr):
    testStr = testStr.replace(" each",' 1 Each').strip().replace("|each",' 1 Each')
    newStrList = []
    [newStrList.append(i) for i in testStr.replace("/",' ').split(" ") if i not in newStrList]
    newStrList = [i.strip() for i in newStrList if i.strip()!='']
    return " ".join(newStrList)

def removeLastSFromTitle(tempList):
    s_keywords = ['peppers','mushrooms','carrots','potatoes','tomatoes','cuts','apples','beets',
    'onions','lemons','beans','limes','cucumbers','keylimes','mangos','papayas',
    'coconuts','sprouts','oranges']
    newTi = []
    for i in tempList:
        if i in s_keywords:
            newTi.append(i.replace("s",''))
        else:
            newTi.append(i)
    newTi = list(set(newTi))
    newTi.sort()
    return " ".join(newTi)

def getAimleapId(NewTitle):
    try:
        aimleapId = NewTitlesdf[NewTitlesdf['title']==NewTitle]['aimleapId'].iloc[0]
    except:
        aimleapId = ""
    return aimleapId
# 1.target
# 2.jewel
# 3.marinos
# 4.walmart
# oldUpc = "m0003338301724 | w0008523904943| m0008523904943"
def getUpc(oldUpc):
    testList = oldUpc.split("|")
    testList = [i.strip() for i in testList]
    tempList = [i[0] for i in testList]
    if len(list(set(tempList)))!=1:
        if 't' in tempList:
            upc = testList[tempList.index('t')]
        elif 'j' in tempList:
            upc = testList[tempList.index('j')]
        elif 'm' in tempList:
            upc = testList[tempList.index('m')]
        elif 'w' in tempList:
            upc = testList[tempList.index('w')]
    else:
        upc = oldUpc
    return upc
def getUrls(url):
    urls = [i.strip() for i in url.split("|")]
    jewelList = "|".join([i for i in urls if "jewel" in i])
    walmartList = "|".join([i for i in urls if "walmart" in i])
    marianosList = "|".join([i for i in urls if "marianos" in i])
    targetList = "|".join([i for i in urls if "target" in i])
    return jewelList,walmartList,marianosList,targetList

def getUpcs(str_):
    x = str_.split("|")[0]
    if len(x)<13:
        return "".join(["0" for i in range(13-len(x))])+x+"^"
    else:
        return x +"^"

def getCleannationalBrand(nationalBrand):
    nationalBrandgrupd1 = nationalBrand.groupby("NewTitle").aggregate(lambda x: ' | '.join(set(map(str, x)))).reset_index()
    nationalBrandgrupd1 = nationalBrandgrupd1[nationalBrandgrupd1['aimleapId']!='']
    nationalBrandgrupd1['upcPipeline'] = nationalBrandgrupd1['upc'].apply(lambda x:"yes" if "|" in x else "no")
    nationalBrandgrupd1['stdUPC'] = nationalBrandgrupd1['newUpc'].apply(lambda x:getUpc(x))
    del nationalBrandgrupd1['source']
    del nationalBrandgrupd1['newUpc']
    del nationalBrandgrupd1['upcPipeline']
    nationalBrandgrupd1['spaceInNewTitle'] = nationalBrandgrupd1['NewTitle'].apply(lambda x:"yes" if " " in x else "no")
    nationalBrandgrupd1 = nationalBrandgrupd1[nationalBrandgrupd1['spaceInNewTitle'] == 'yes']
    del nationalBrandgrupd1['spaceInNewTitle']
    nationalBrandgrupd = nationalBrandgrupd1[['NewTitle','product_title','url','stdUPC','brandStatus']]

    nationalBrandgrupd['tempurl'] = nationalBrandgrupd['url'].apply(lambda x:getUrls(x))
    nationalBrandgrupd['jewel_url'] = nationalBrandgrupd['tempurl'].apply(lambda x:x[0])
    nationalBrandgrupd['marianos_url'] = nationalBrandgrupd['tempurl'].apply(lambda x:x[2])
    nationalBrandgrupd['target_url'] = nationalBrandgrupd['tempurl'].apply(lambda x:x[3])
    nationalBrandgrupd['walmart_url'] = nationalBrandgrupd['tempurl'].apply(lambda x:x[1])
    del nationalBrandgrupd['tempurl']


    nationalBrandgrupd['UPC'] = nationalBrandgrupd['stdUPC'].apply(lambda x:getUpcs(x[1:]))
    del nationalBrandgrupd['stdUPC']
    del nationalBrandgrupd['url']
    nationalBrandgrupd['mappedStatus'] = nationalBrandgrupd['product_title'].apply(lambda x:"yes" if "|" in x else "no")
    nationalNotMapped = nationalBrandgrupd[nationalBrandgrupd['mappedStatus']=='no']
    nationalBrandgrupd = nationalBrandgrupd[nationalBrandgrupd['mappedStatus']=='yes']
    del nationalBrandgrupd['mappedStatus']
    return nationalBrandgrupd

def getCleanstoreBrand(storeBrand):
    storeBrandgrupd1 = storeBrand.groupby("NewTitle").aggregate(lambda x: ' | '.join(set(map(str, x)))).reset_index()
    storeBrandgrupd1 = storeBrandgrupd1[storeBrandgrupd1['aimleapId']!='']
    storeBrandgrupd1['upcPipeline'] = storeBrandgrupd1['upc'].apply(lambda x:"yes" if "|" in x else "no")
    storeBrandgrupd1['stdUPC'] = storeBrandgrupd1['newUpc'].apply(lambda x:getUpc(x))
    del storeBrandgrupd1['source']
    del storeBrandgrupd1['newUpc']
    del storeBrandgrupd1['upcPipeline']
    storeBrandgrupd1['spaceInNewTitle'] = storeBrandgrupd1['NewTitle'].apply(lambda x:"yes" if " " in x else "no")
    storeBrandgrupd1 = storeBrandgrupd1[storeBrandgrupd1['spaceInNewTitle'] == 'yes']
    del storeBrandgrupd1['spaceInNewTitle']
    storeBrandgrupd = storeBrandgrupd1[['NewTitle','product_title','url','stdUPC','brandStatus']]

    storeBrandgrupd['tempurl'] = storeBrandgrupd['url'].apply(lambda x:getUrls(x))

    storeBrandgrupd['jewel_url'] = storeBrandgrupd['tempurl'].apply(lambda x:x[0])
    storeBrandgrupd['marianos_url'] = storeBrandgrupd['tempurl'].apply(lambda x:x[2])
    storeBrandgrupd['target_url'] = storeBrandgrupd['tempurl'].apply(lambda x:x[3])
    storeBrandgrupd['walmart_url'] = storeBrandgrupd['tempurl'].apply(lambda x:x[1])
    del storeBrandgrupd['tempurl']


    storeBrandgrupd['UPC'] = storeBrandgrupd['stdUPC'].apply(lambda x:getUpcs(x[1:]))
    del storeBrandgrupd['stdUPC']
    del storeBrandgrupd['url']
    storeBrandgrupd['mappedStatus'] = storeBrandgrupd['product_title'].apply(lambda x:"yes" if "|" in x else "no")
    storeNotMapped = storeBrandgrupd[storeBrandgrupd['mappedStatus']=='no']

    storeBrandgrupd = storeBrandgrupd[storeBrandgrupd['mappedStatus']=='yes']
    del storeBrandgrupd['mappedStatus']
    return storeBrandgrupd

def getCleanOrganic(organic):
    organicgrupd1 = organic.groupby("NewTitle").aggregate(lambda x: ' | '.join(set(map(str, x)))).reset_index()
    organicgrupd1 = organicgrupd1[organicgrupd1['aimleapId']!='']
    organicgrupd1['upcPipeline'] = organicgrupd1['upc'].apply(lambda x:"yes" if "|" in x else "no")
    organicgrupd1['stdUPC'] = organicgrupd1['newUpc'].apply(lambda x:getUpc(x))
    del organicgrupd1['source']
    del organicgrupd1['newUpc']
    del organicgrupd1['upcPipeline']
    organicgrupd1['spaceInNewTitle'] = organicgrupd1['NewTitle'].apply(lambda x:"yes" if " " in x else "no")
    organicgrupd1 = organicgrupd1[organicgrupd1['spaceInNewTitle'] == 'yes']
    del organicgrupd1['spaceInNewTitle']
    organicgrupd = organicgrupd1[['NewTitle','product_title','url','stdUPC','brandStatus']]

    organicgrupd['tempurl'] = organicgrupd['url'].apply(lambda x:getUrls(x))
    organicgrupd['jewel_url'] = organicgrupd['tempurl'].apply(lambda x:x[0])
    organicgrupd['marianos_url'] = organicgrupd['tempurl'].apply(lambda x:x[2])
    organicgrupd['target_url'] = organicgrupd['tempurl'].apply(lambda x:x[3])
    organicgrupd['walmart_url'] = organicgrupd['tempurl'].apply(lambda x:x[1])
    del organicgrupd['tempurl']


    organicgrupd['UPC'] = organicgrupd['stdUPC'].apply(lambda x:getUpcs(x[1:]))
    del organicgrupd['stdUPC']
    del organicgrupd['url']
    organicgrupd['mappedStatus'] = organicgrupd['product_title'].apply(lambda x:"yes" if "|" in x else "no")
    organicNotMapped = organicgrupd[organicgrupd['mappedStatus']=='no']
    organicgrupd = organicgrupd[organicgrupd['mappedStatus']=='yes']
    del organicgrupd['mappedStatus']
    return organicgrupd



def main():
    #store brand selection
    marianos = ["Private Selection", "Kroger", "Simple Truth"]
    # marianos = ["Private Selection", "Kroger", "Simple Truth", "Simple Truth Organic"]
    Target = ["Deal Worthy", "Good & Gather", "Market Pantry", "Favorite Day", "Kindfull", "Smartly", "Up & Up"]
    # Jewel =  ['Lucerne', "Signature Select", "O Organics", "Open Nature", "Waterfront Bistro", "Primo Taglio",
    #           "Soleil", "Value Corner", "Ready Meals"]
    Jewel =  ['Lucerne', "Signature Select", "Open Nature", "Waterfront Bistro", "Primo Taglio",
              "Soleil", "Value Corner", "Ready Meals"]
    Walmart = ["Clear American", "Great Value", "Home Bake Value", "Marketside",
               "Co Squared", "Best Occasions", "Mash-Up Coffee", "World Table"]

    organiclist = ["Simple Truth Organic", "O Organics"]
    storeBrandList = []
    [storeBrandList.append(i) for i in marianos]
    [storeBrandList.append(i) for i in Target]
    [storeBrandList.append(i) for i in Jewel]
    [storeBrandList.append(i) for i in Walmart]
    #curation input file
    curationFile = "PASS CURATION FILE"

    variationsDf = pd.read_excel(curationFile)
    variationsDf = variationsDf.fillna("")

    cate1List = variationsDf['cat1'].unique()
    cate2List = variationsDf['cat2'].unique()
    cate3List = variationsDf['cat3'].unique()
    cate4List = variationsDf['cat4'].unique()

    labels1 = variationsDf['label1'].unique()
    labels2 = variationsDf['label2'].unique()
    form1 = list(variationsDf['form1'].unique())
    form2 = list(variationsDf['form2'].unique())
    form3 = list(variationsDf['form3'].unique())

    [form1.append(i) for i in form2]
    [form1.append(i) for i in form3]
    forms = list(set(form1))

    forms = [i.lower().strip() for i in forms if i!='']
    cate1List = [i.lower().strip() for i in cate1List if i!='']
    cate2List = [i.lower().strip() for i in cate2List if i!='']
    cate3List = [i.lower().strip() for i in cate3List if i!='']
    cate4List = [i.lower().strip() for i in cate4List if i!='']
    labels1 = [i.lower().strip() for i in labels1 if i!='']
    labels2 = [i.lower().strip() for i in labels2 if i!='']


    withList = variationsDf['with'].unique()
    # FlavorList = variationsDf['Flavor'].unique()
    PackList = variationsDf['Pack'].unique()
    withList = [i.lower().strip() for i in withList if i!='']
    # FlavorList = [i.lower().strip() for i in FlavorList if i!='']
    PackList = [i.lower().strip() for i in PackList if i!='']


    inputFile = "PASS_HERE_OUTPUT_FILE .json"
    combinedDf = pd.read_json(inputFile)
    combinedDf = combinedDf.fillna("")
    produceDf = selectCategories(combinedDf)
    produceDf = produceDf.reset_index(drop=True)
    produceDf = produceDf.drop_duplicates(keep='first')
    produceDf['product_title_weight'] = produceDf['product_title'] + " "+produceDf['weight']
    produceDf[['Weight_', 'Count_']] = produceDf['product_title_weight'].apply(lambda x: pd.Series(extract_weight_count(x)))
    produceDf['brandStatus'] = produceDf['product_title'].apply(lambda x:getStoreBrand(storeBrandList,x,organiclist))
    produceDf['aimleapTitle'] = produceDf['product_title'].apply(lambda x:getAimleapTitle(x.lower()))
    produceDf['Weight_'] = produceDf['Weight_'].apply(lambda x:x.lower().replace(" ",'').strip())
    produceDf['Count_'] = produceDf['Count_'].apply(lambda x:x.lower().replace("1 count",'1 each').strip())
    produceDf['Count_'] = produceDf['Count_'].apply(lambda x:x.replace("1 each",''))
    produceDf['aimleapTitle'] = produceDf['aimleapTitle']+" "+produceDf['Weight_']+" "+produceDf['Count_']
    produceDf['aimleapTitle'] = produceDf['aimleapTitle'].apply(lambda x:x.strip())
    produceDf['aimleapTitle'] = produceDf['aimleapTitle'].apply(lambda x:x.strip())
    produceDf['aimleapTitle'] = produceDf['aimleapTitle'].apply(lambda x:getNewStr(x))
    produceDf['aimleapTitle'] = produceDf['aimleapTitle'].apply(lambda x:cleanTitle(x).replace(" package",'').replace('|package',''))
    produceDf = produceDf.rename(columns={"aimleapTitle":"NewTitle"})
    produceDf = produceDf.reset_index(drop=True)
    NewTitles = produceDf['NewTitle'].unique()
    aimleapIds = ["Aimleap"+str(i) for i in range(len(NewTitles))]
    aimleapIdsdf = pd.DataFrame(aimleapIds,columns=['aimleapId'])
    NewTitlesdf = pd.DataFrame(NewTitles,columns=['title'])
    NewTitlesdf['aimleapId'] = aimleapIdsdf['aimleapId']
    produceDf['aimleapId'] = produceDf['NewTitle'].apply(lambda x:getAimleapId(x))
    produceDf['source'] = produceDf['url'].apply(lambda x:x.split("/")[2])
    produceDf['source'] = produceDf['source'].apply(lambda x:x.split(".")[1])
    produceDf['newUpc'] = produceDf.apply(lambda x:x['source'][0]+str(x['upc']),axis=1)

    nationalBrand = produceDf[produceDf['brandStatus']=='national brand']
    storeBrand = produceDf[produceDf['brandStatus']=='store brand']
    organic = produceDf[produceDf['brandStatus']=='organic']

    nationalBrandgrupd = getCleannationalBrand(nationalBrand)
    storeBrandgrupd = getCleanstoreBrand(storeBrand)
    organicgrupd = getCleanOrganic(organic)

    storeBrandgrupd = storeBrandgrupd.append(nationalBrandgrupd)
    storeBrandgrupd = storeBrandgrupd.append(organicgrupd)
    storeBrandgrupd = storeBrandgrupd.reset_index(drop=True)
    del storeBrandgrupd['NewTitle']
    storeNotMapped = storeNotMapped.append(nationalNotMapped)
    storeNotMapped = storeNotMapped.append(organicNotMapped)
    storeBrandgrupd['jewel_url'] = storeBrandgrupd['jewel_url'].apply(lambda x:x.replace("|","\n"))
    storeBrandgrupd['marianos_url'] = storeBrandgrupd['marianos_url'].apply(lambda x:x.replace("|","\n"))
    storeBrandgrupd['target_url'] = storeBrandgrupd['target_url'].apply(lambda x:x.replace("|","\n"))
    storeBrandgrupd['walmart_url'] = storeBrandgrupd['walmart_url'].apply(lambda x:x.replace("|","\n"))
    # Slno
    ids = [i+1 for i in range(len(storeBrandgrupd))]
    ids = pd.DataFrame(ids,columns=['Sl.No'])
    storeBrandgrupd['Sl.No'] = ids['Sl.No']
    storeBrandgrupd = storeBrandgrupd[['Sl.No','product_title', 'brandStatus', 'jewel_url', 'marianos_url',
           'target_url', 'walmart_url', 'UPC']]

    # with pd.ExcelWriter("classification_produce_"+str(datetime.now().date())+".xlsx",engine='xlsxwriter',options={"strings_to_urls":False}) as writer:
    #     storeBrandgrupd.to_excel(writer,index=False)
    storeBrandgrupd['jewel_urlCount'] = storeBrandgrupd['jewel_url'].apply(lambda x:0 if x=='' else 1)
    storeBrandgrupd['marianos_urlCount'] = storeBrandgrupd['marianos_url'].apply(lambda x:0 if x=='' else 1)
    storeBrandgrupd['target_urlCount'] = storeBrandgrupd['target_url'].apply(lambda x:0 if x=='' else 1)
    storeBrandgrupd['walmart_urlCount'] = storeBrandgrupd['walmart_url'].apply(lambda x:0 if x=='' else 1)
    storeBrandgrupd['count'] = storeBrandgrupd['jewel_urlCount']+storeBrandgrupd['marianos_urlCount']+storeBrandgrupd['target_urlCount']+storeBrandgrupd['walmart_urlCount']
    storeBrandgrupd = storeBrandgrupd[storeBrandgrupd['count']>=2]
    storeBrandgrupd = storeBrandgrupd.reset_index(drop=True)
    storeBrandgrupd = storeBrandgrupd[['Sl.No', 'product_title', 'brandStatus', 'jewel_url', 'marianos_url','target_url', 'walmart_url', 'UPC']]
    # Slno
    ids = [i+1 for i in range(len(storeBrandgrupd))]
    ids = pd.DataFrame(ids,columns=['Sl.No'])
    storeBrandgrupd['Sl.No'] = ids['Sl.No']
    with pd.ExcelWriter("classification_produce_"+str(datetime.now().date())+".xlsx",engine='xlsxwriter',options={"strings_to_urls":False}) as writer:
        storeBrandgrupd.to_excel(writer,index=False)


if __name__ == '__main__':
    main()
