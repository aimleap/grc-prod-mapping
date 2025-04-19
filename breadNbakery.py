#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
from datetime import datetime

def getBrands():
    #store brand selection 
    marianos = ["Private Selection", "Kroger", "Simple Truth", "Simple Truth Organic"]
    Target = ["Deal Worthy", "Good & Gather", "Market Pantry", "Favorite Day", "Kindfull", "Smartly", "Up & Up"]
    Jewel =  ['Lucerne', "Signature Select", "O Organics", "Open Nature", "Waterfront Bistro", "Primo Taglio",
              "Soleil", "Value Corner", "Ready Meals"]
    Walmart = ["Clear American", "Great Value", "Home Bake Value", "Marketside", 
               "Co Squared", "Best Occasions", "Mash-Up Coffee", "World Table"]

    storeBrandList = []
    [storeBrandList.append(i) for i in marianos]
    [storeBrandList.append(i) for i in Target]
    [storeBrandList.append(i) for i in Jewel]
    [storeBrandList.append(i) for i in Walmart]
    return storeBrandList

def extract_weight_count(product):
    weight = ""
    count = ""
     # Match weight with optional space and decimal support
    weight_match = re.search(r'(\d+(\.\d+)?)\s?oz', product, re.IGNORECASE)
    # Match count with optional space and variations of 'ct', 'Count', and 'Each'
    count_match = re.search(r'(\d+)?\s?(Count|ct|Each)', product, re.IGNORECASE)
    
    if weight_match:
        weight = weight_match.group(0).strip()
    
    if count_match:
        count_num = count_match.group(1)
        if count_num:
            count = count_num.strip() + ' Count'
        else:
            count = '1 Each'
    
    return weight, count

def getStoreBrand(storeBrandList,title):
    # BASED ON TITLE CHECK BRAND 
    storeBrand = [brand for brand in storeBrandList if brand in title]
    if len(storeBrand)==0:
        status = "national brand"
    else:
        status = "store brand"
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
    testString = testString.lower().replace(","," ").replace("!",' ').replace("("," ").replace(")",' ').replace("."," ").replace('"',' ')
    if "pastries" in testString:
        testString = testString.replace("pastries","pastry")
    if "strawberries" in testString:
        testString = testString.replace("strawberries","strawberry")
    if "inches" in testString:
        testString = testString.replace("inches","inch")
    #  "pastries":"Pastry",'strawberries',"Strawberry"
    cate1 = getAvailableString(cate1List,testString)
    cate2 = getAvailableString(cate2List,testString)
    cate3 = getAvailableString(cate3List,testString)
    cate4 = getAvailableString(cate4List,testString)
    cate5 = getAvailableString(cate5List,testString)

    form1 = getAvailableString(forms,testString)
    label1 = getAvailableString(labels,testString)
    label2 = getAvailableString(labels2,testString)
    with_ = getAvailableString(withList,testString)
    flavor = getAvailableString(FlavorList,testString)
    pack = getAvailableString(PackList,testString)
    
    aimleapTitleList = []
    aimleapTitleList.append(cate1)
    if cate2 not in aimleapTitleList:
        aimleapTitleList.append(cate2)
    if cate3 not in aimleapTitleList:
        aimleapTitleList.append(cate3)
    if cate4 not in aimleapTitleList:
        aimleapTitleList.append(cate4)
    if cate5 not in aimleapTitleList:
        aimleapTitleList.append(cate5)
    if form1 not in aimleapTitleList:
        aimleapTitleList.append(form1)
        
    if label1 not in aimleapTitleList:
        aimleapTitleList.append(label1)
    if label2 not in aimleapTitleList:
        aimleapTitleList.append(label2)

    if with_ not in aimleapTitleList:
        aimleapTitleList.append(with_)
    if flavor not in aimleapTitleList:
        aimleapTitleList.append(flavor)
    if pack not in aimleapTitleList:
        aimleapTitleList.append(pack)

    aimleapTitle = " ".join([i for i in aimleapTitleList if i!=''])
    newTitle = []
    [newTitle.append(i) for i in aimleapTitle.lower().split(" ") if i not in newTitle]
    if "-" in newTitle:
        newTitle.remove("-")
    if "&" in newTitle:
        newTitle.remove("&")
    if "and" in newTitle:
        newTitle.remove("and")
        
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
    s_keywords = ["cookies","muffins","bites",'donuts','cupcakes','bagels','tortillas','pies','slices','chunks','oranges','grains','rounds','sheets',
                 'baguettes','brownies','minis']
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
    nationalBrandgrupd = nationalBrandgrupd1[['NewTitle','product_title','url','stdUPC','brandStatus','aimleapTitlewithsource']]

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
    storeBrandgrupd = storeBrandgrupd1[['NewTitle','product_title','url','stdUPC','brandStatus','aimleapTitlewithsource']]

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
    storeBrandgrupd = storeBrandgrupd[storeBrandgrupd['mappedStatus']=='yes']
    del storeBrandgrupd['mappedStatus']
    return storeBrandgrupd


storeBrandList = getBrands()
inputFile = "PASS_HERE_OUTPUT_FILE .json"
bakeryDf = pd.read_json(inputFile)
bakeryDf = bakeryDf.fillna("")
#category selectiong
bakeryDf = bakeryDf[(bakeryDf['category']=='Bakery & Bread') | (bakeryDf['category']=='Bread & Bakery')| (bakeryDf['category']=='Bakery')]
bakeryDf['source'] = bakeryDf['url'].apply(lambda x:x.split(".com")[0].split(".")[-1])
bakeryDf['product_title_weight'] = bakeryDf['product_title'] + " "+bakeryDf['weight']
bakeryDf[['Weight_', 'Count_']] = bakeryDf['product_title_weight'].apply(lambda x: pd.Series(extract_weight_count(x)))
bakeryDf['brandStatus'] = bakeryDf['product_title'].apply(lambda x:getStoreBrand(storeBrandList,x))
bakeryDf['aimleapTitle'] = bakeryDf['product_title'].apply(lambda x:getAimleapTitle(x.lower()))    
#curation input file
curationFile = "PASS CURATION FILE"
variationsDf = pd.read_excel(curationFile)
variationsDf = variationsDf.fillna("")
cate1List = variationsDf['Cat1'].unique()
cate2List = variationsDf['Cat2'].unique()
cate3List = variationsDf['Cat3'].unique()
cate4List = variationsDf['Cat4'].unique()
cate5List = variationsDf['Cat5'].unique()

labels = variationsDf['Labels'].unique()
labels2 = variationsDf['label2'].unique()
form1 = list(variationsDf['Form1'].unique())
form2 = list(variationsDf['Form2'].unique())
form3 = list(variationsDf['Form3'].unique())
form4 = list(variationsDf['Form4'].unique())

[form1.append(i) for i in form2]
[form1.append(i) for i in form3]
[form1.append(i) for i in form4]
forms = list(set(form1))

forms = [i.lower().strip() for i in forms if i!='']
cate1List = [i.lower().strip() for i in cate1List if i!='']
cate2List = [i.lower().strip() for i in cate2List if i!='']
cate3List = [i.lower().strip() for i in cate3List if i!='']
cate4List = [i.lower().strip() for i in cate4List if i!='']
cate5List = [i.lower().strip() for i in cate5List if i!='']
labels = [i.lower().strip() for i in labels if i!='']
labels2 = [i.lower().strip() for i in labels2 if i!='']


withList = variationsDf['with'].unique()
FlavorList = variationsDf['Flavor'].unique()
PackList = variationsDf['Pack'].unique()
withList = [i.lower().strip() for i in withList if i!='']
FlavorList = [i.lower().strip() for i in FlavorList if i!='']
PackList = [i.lower().strip() for i in PackList if i!='']


bakeryDf['Weight_'] = bakeryDf['Weight_'].apply(lambda x:x.lower().replace(" ",'').strip())
bakeryDf['Count_'] = bakeryDf['Count_'].apply(lambda x:x.lower().replace("1 Count",'1 Each').strip())
bakeryDf['aimleapTitle'] = bakeryDf['aimleapTitle']+" "+bakeryDf['Weight_']+" "+bakeryDf['Count_']
bakeryDf['aimleapTitle'] = bakeryDf['aimleapTitle'].apply(lambda x:x.strip())
bakeryDf['aimleapTitle'] = bakeryDf['aimleapTitle'].apply(lambda x:x.strip())
bakeryDf['aimleapTitle'] = bakeryDf['aimleapTitle'].apply(lambda x:getNewStr(x))
bakeryDf['aimleapTitle'] = bakeryDf['aimleapTitle'].apply(lambda x:cleanTitle(x).replace(" package",'').replace('|package',''))
bakeryDf = bakeryDf.rename(columns={"aimleapTitle":"NewTitle"})
bakeryDf = bakeryDf.reset_index(drop=True)
NewTitles = bakeryDf['NewTitle'].unique()
aimleapIds = ["Aimleap"+str(i) for i in range(len(NewTitles))]
aimleapIdsdf = pd.DataFrame(aimleapIds,columns=['aimleapId'])
NewTitlesdf = pd.DataFrame(NewTitles,columns=['title'])
NewTitlesdf['aimleapId'] = aimleapIdsdf['aimleapId']
bakeryDf['aimleapId'] = bakeryDf['NewTitle'].apply(lambda x:getAimleapId(x))
bakeryDf['source'] = bakeryDf['url'].apply(lambda x:x.split("/")[2])
bakeryDf['source'] = bakeryDf['source'].apply(lambda x:x.split(".")[1])
bakeryDf['aimleapTitlewithsource'] = bakeryDf['product_title'] +" + "+ bakeryDf['source']

bakeryDf['newUpc'] = bakeryDf.apply(lambda x:x['source'][0]+str(x['upc']),axis=1)
nationalBrand = bakeryDf[bakeryDf['brandStatus']=='national brand']
storeBrand = bakeryDf[bakeryDf['brandStatus']=='store brand']
nationalBrandgrupd = getCleannationalBrand(nationalBrand)
storeBrandgrupd = getCleanstoreBrand(storeBrand)

storeBrandgrupd = storeBrandgrupd.append(nationalBrandgrupd)
storeBrandgrupd = storeBrandgrupd.reset_index(drop=True)
del storeBrandgrupd['NewTitle']

storeBrandgrupd['jewel_url'] = storeBrandgrupd['jewel_url'].apply(lambda x:x.replace("|","\n"))
storeBrandgrupd['marianos_url'] = storeBrandgrupd['marianos_url'].apply(lambda x:x.replace("|","\n"))
storeBrandgrupd['target_url'] = storeBrandgrupd['target_url'].apply(lambda x:x.replace("|","\n"))
storeBrandgrupd['walmart_url'] = storeBrandgrupd['walmart_url'].apply(lambda x:x.replace("|","\n"))

# Slno
ids = [i+1 for i in range(len(storeBrandgrupd))]
ids = pd.DataFrame(ids,columns=['Sl.No'])
storeBrandgrupd['Sl.No'] = ids['Sl.No']
storeBrandgrupd = storeBrandgrupd[['Sl.No','product_title', 'brandStatus', 'jewel_url', 'marianos_url',
       'target_url', 'walmart_url', 'UPC','aimleapTitlewithsource']]

# with pd.ExcelWriter("classification_breadNbakery_"+str(datetime.now().date())+".xlsx",engine='xlsxwriter',options={"strings_to_urls":False}) as writer:
#     storeBrandgrupd.to_excel(writer,index=False)

storeBrandgrupd = storeBrandgrupd.fillna("")
storeBrandgrupd['jewel_urlCount'] = storeBrandgrupd['jewel_url'].apply(lambda x:0 if x=='' else 1)
storeBrandgrupd['marianos_urlCount'] = storeBrandgrupd['marianos_url'].apply(lambda x:0 if x=='' else 1)
storeBrandgrupd['target_urlCount'] = storeBrandgrupd['target_url'].apply(lambda x:0 if x=='' else 1)
storeBrandgrupd['walmart_urlCount'] = storeBrandgrupd['walmart_url'].apply(lambda x:0 if x=='' else 1)
storeBrandgrupd['count'] = storeBrandgrupd['jewel_urlCount']+storeBrandgrupd['marianos_urlCount']+storeBrandgrupd['target_urlCount']+storeBrandgrupd['walmart_urlCount']
storeBrandgrupd = storeBrandgrupd[storeBrandgrupd['count']>=2]
storeBrandgrupd = storeBrandgrupd.reset_index(drop=True)
storeBrandgrupd = storeBrandgrupd[['Sl.No', 'product_title', 'brandStatus', 'jewel_url', 'marianos_url','target_url', 'walmart_url', 'UPC','aimleapTitlewithsource']]
# Slno
ids = [i+1 for i in range(len(storeBrandgrupd))]
ids = pd.DataFrame(ids,columns=['Sl.No'])
storeBrandgrupd['Sl.No'] = ids['Sl.No']
storeBrandgrupd = storeBrandgrupd[['Sl.No', 'product_title', 'brandStatus', 'jewel_url', 'marianos_url','target_url', 'walmart_url', 'UPC']]
with pd.ExcelWriter("classification_breadNbakery_"+str(datetime.now().date())+".xlsx",engine='xlsxwriter',options={"strings_to_urls":False}) as writer:
    storeBrandgrupd.to_excel(writer,index=False)
    
def getSourceWiseProducts(testString):
    testStringList = testString.split("|")
    marianosProducts = "|".join([i.replace("+ marianos",'').strip() for i in testStringList if "marianos" in i])
    jeweloscoProducts = "|".join([i.replace("+ jewelosco",'').strip() for i in testStringList if "jewelosco" in i])
    targetProducts = "|".join([i.replace("+ target",'').strip() for i in testStringList if "target" in i])
    walmartProducts = "|".join([i.replace("+ walmart",'').strip() for i in testStringList if "walmart" in i])
    return marianosProducts, jeweloscoProducts, targetProducts,walmartProducts


storeBrandgrupd['aimleapTitlewithsourceSET'] = storeBrandgrupd['aimleapTitlewithsource'].apply(lambda x:getSourceWiseProducts(x))
storeBrandgrupd['Mariano Product'] = storeBrandgrupd['aimleapTitlewithsourceSET'].apply(lambda x:x[0])
storeBrandgrupd['Jewelosco Product'] = storeBrandgrupd['aimleapTitlewithsourceSET'].apply(lambda x:x[1])
storeBrandgrupd['Target Product'] = storeBrandgrupd['aimleapTitlewithsourceSET'].apply(lambda x:x[2])
storeBrandgrupd['Walmart Product'] = storeBrandgrupd['aimleapTitlewithsourceSET'].apply(lambda x:x[3])
storeBrandgrupd['Common UPC'] = storeBrandgrupd['UPC']
productMtchingDf = storeBrandgrupd[['Common UPC','Walmart Product','Target Product','Mariano Product','Jewelosco Product']]

    
with pd.ExcelWriter("breadNbakeryProductMatching_"+str(datetime.now().date())+".xlsx",engine='xlsxwriter',options={"strings_to_urls":False}) as writer:
    productMtchingDf.to_excel(writer,index=False)


# In[1]:




