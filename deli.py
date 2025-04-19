#!/usr/bin/env python
# coding: utf-8

# In[2]:


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

def getStoreBrand(storeBrandList,title):
    storeBrand = [brand for brand in storeBrandList if brand in title]
    if len(storeBrand)==0:
        status = "national brand"
    else:
        status = "store brand"
    return status

def extract_weight_count(product):

    weight = ""
    count = ""
     # Match weight with optional space and decimal support
#     weight_match = re.search(r'(\d+(\.\d+)?)\s?oz', product, re.IGNORECASE)
    weight_match = re.search(r'(\d+(\.\d+)?)\s?(oz|lb|lbs)', product, re.IGNORECASE)

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

def getCleanVariations(formList):
    formList = [i for i in formList if i not in smoked]
    formList = [i for i in formList if i not in cured]
    formList = [i for i in formList if i not in boneIn]
    formList = [i for i in formList if i not in boneless]
    formList = [i for i in formList if i not in deliSlices]
    formList = [i for i in formList if i not in cuts]
    formList = [i for i in formList if i not in numbers]
    return formList

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
    cate1 = getAvailableString(cate1List,testString)
    cate2 = getAvailableString(cate2List,testString)
    cate3 = getAvailableString(cate3List,testString)
    cate4 = getAvailableString(cate4List,testString)

    form1 = getAvailableString(form1List,testString)

    form2 = getAvailableString(form2List,testString)

    form3 = getAvailableString(form3List,testString)

    form4 = getAvailableString(form4List,testString)

    label1 = getAvailableString(label1List,testString)
    label2 = getAvailableString(label2List,testString)
    label3 = getAvailableString(label3List,testString)
    
    smoked_ = getAvailableString(smoked,testString)
    cured_ = getAvailableString(cured,testString)
    boneIn_ = getAvailableString(boneIn,testString)
    boneless_ = getAvailableString(boneless,testString)
    deliSlices_ = getAvailableString(deliSlices,testString)
    cuts_ = getAvailableString(cuts,testString)
    numbers_ = getAvailableString(numbers,testString)
    newCate_ = getAvailableString(newCate,testString)
    newForm_ = getAvailableString(newForm,testString)
    newLable_ = getAvailableString(newLable,testString)
    
    

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
    if form2 not in aimleapTitleList:
        aimleapTitleList.append(form2)
    if form3 not in aimleapTitleList:
        aimleapTitleList.append(form3)
    if form4 not in aimleapTitleList:
        aimleapTitleList.append(form4)
        
    if label1 not in aimleapTitleList:
        aimleapTitleList.append(label1)
    if label2 not in aimleapTitleList:
        aimleapTitleList.append(label2)
    if label3 not in aimleapTitleList:
        aimleapTitleList.append(label3)
        
    if smoked_ not in aimleapTitleList:
        aimleapTitleList.append(smoked_)
    if cured_ not in aimleapTitleList:
        aimleapTitleList.append(cured_)
    if boneIn_ not in aimleapTitleList:
        aimleapTitleList.append(boneIn_)
    if boneless_ not in aimleapTitleList:
        aimleapTitleList.append(boneless_)
    if deliSlices_ not in aimleapTitleList:
        aimleapTitleList.append(deliSlices_)
    if cuts_ not in aimleapTitleList:
        aimleapTitleList.append(cuts_)
    if numbers_ not in aimleapTitleList:
        aimleapTitleList.append(numbers_)
        
    if newCate_ not in aimleapTitleList:
        aimleapTitleList.append(newCate_)
    if newForm_ not in aimleapTitleList:
        aimleapTitleList.append(newForm_)    
    if newLable_ not in aimleapTitleList:
        aimleapTitleList.append(newLable_)
        


    aimleapTitle = " ".join([i for i in aimleapTitleList if i!=''])
    newTitle = []
    [newTitle.append(i) for i in aimleapTitle.lower().split(" ") if i not in newTitle]
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
    return " ".join(newTitle)

def cleanTitle(testStr):
    newtestStr = getNewStr(testStr)
    if "1 Each" in newtestStr:
        newtestStr = newtestStr.replace(" 1 Each",'').strip()+" 1 Each"
    return newtestStr

def getNewStr(testStr):
    testStr = testStr.replace(" each",' 1 Each').strip().replace("|each",' 1 Each')
#     testStr = testStr.replace("each 1count", "1 each").strip()
    newStrList = []
    [newStrList.append(i) for i in testStr.replace("/",' ').split(" ") if i not in newStrList]
    newStrList = [i.strip() for i in newStrList if i.strip()!='']
    return " ".join(newStrList)

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
    nationalBrandgrupd = nationalBrandgrupd1[['NewTitle','product_title','url','stdUPC','brandStatus','weight','aimleapTitlewithsource']]

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
    return nationalBrandgrupd1

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
    storeBrandgrupd = storeBrandgrupd1[['NewTitle','product_title','url','stdUPC','brandStatus','weight','aimleapTitlewithsource']]

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
    return storeBrandgrupd1

inputFile = "PASS_HERE_OUTPUT_FILE .json"

deliDf = pd.read_json(inputFile)
deliDf = deliDf.fillna("")
#category selectiong
# Meat & Seafood
# Deli
deliDf = deliDf[(deliDf['category']=='Meat & Seafood') | (deliDf['category']=='Deli')]

#curation input file
curationFile1 = "PASS CURATION FILE"
variation1df = pd.read_excel(curationFile1)
variation1df = variation1df.fillna("")
#clean curation file
cate1List = [i.strip().lower() for i in variation1df['Cat1'].unique() if i.strip()!='']
cate2List = [i.strip().lower() for i in variation1df['Cat2'].unique() if i.strip()!='']
cate3List = [i.strip().lower() for i in variation1df['Cat3'].unique() if i.strip()!='']
cate4List = [i.strip().lower() for i in variation1df['Cat4'].unique() if i.strip()!='']

form1List = [i.strip().lower() for i in variation1df['Form1'].unique() if i.strip()!='']
form2List = [i.strip().lower() for i in variation1df['Form2'].unique() if i.strip()!='']
form3List = [i.strip().lower() for i in variation1df['Form3'].unique() if i.strip()!='']
form4List = [i.strip().lower() for i in variation1df['Form4'].unique() if i.strip()!='']

label1List = [i.strip().lower() for i in variation1df['Label1'].unique() if i.strip()!='']
label2List = [i.strip().lower() for i in variation1df['Label2'].unique() if i.strip()!='']
label3List = [i.strip().lower() for i in variation1df['Label3'].unique() if i.strip()!='']

cate1List = list(set(cate1List))
cate2List = list(set(cate2List))
cate3List = list(set(cate3List))
cate4List = list(set(cate4List))

form1List = list(set(form1List))
form2List = list(set(form2List))
form3List = list(set(form3List))
form4List = list(set(form4List))

label1List = list(set(label1List))
label2List = list(set(label2List))
label3List = list(set(label3List))


#temporary cleaning
curationFile1 = "PASS CURATION FILE"

variation2df = pd.read_csv(curationFile1)
variation2df = variation2df.fillna("")

smoked = [i.strip().lower() for i in variation2df['smoked'].unique() if i.strip()!='']
cured = [i.strip().lower() for i in variation2df['Cured'].unique() if i.strip()!='']
boneIn = [i.strip().lower() for i in variation2df['Bone In'].unique() if i.strip()!='']
boneless = [i.strip().lower() for i in variation2df['Boneless'].unique() if i.strip()!='']
deliSlices = [i.strip().lower() for i in variation2df['Deli Slices'].unique() if i.strip()!='']
cuts = [i.strip().lower() for i in variation2df['Cuts'].unique() if i.strip()!='']
numbers = [i.strip().lower() for i in variation2df['NUmbers'].unique() if i.strip()!='']

newCate = [i.strip().lower() for i in variation2df['newCate'].unique() if i.strip()!='']
newForm = [i.strip().lower() for i in variation2df['newForm'].unique() if i.strip()!='']
newLable = [i.strip().lower() for i in variation2df['newLable'].unique() if i.strip()!='']

form1List = getCleanVariations(form1List)
form2List = getCleanVariations(form2List)
form3List = getCleanVariations(form3List)
form4List = getCleanVariations(form4List)
label1List = getCleanVariations(label1List)
label2List = getCleanVariations(label2List)
label3List = getCleanVariations(label3List)
cate2List = getCleanVariations(cate2List)
cate1List = getCleanVariations(cate1List)
cate3List = getCleanVariations(cate3List)
cate4List = getCleanVariations(cate4List)

storeBrandList = getBrands()
deliDf['brandStatus'] = deliDf['product_title'].apply(lambda x:getStoreBrand(storeBrandList,x))

deliDf['product_title_weight'] = deliDf['product_title'] + " "+deliDf['weight']
deliDf[['Weight_', 'Count_']] = deliDf['product_title_weight'].apply(lambda x: pd.Series(extract_weight_count(x)))
    
deliDf['aimleapTitle'] = deliDf['product_title'].apply(lambda x:getAimleapTitle(x))
deliDf['Weight_'] = deliDf['Weight_'].apply(lambda x:x.lower().replace(" ",'').strip())
deliDf['Count_'] = deliDf['Count_'].apply(lambda x:x.lower().replace("1 Count",'1 Each').strip())
deliDf['aimleapTitle'] = deliDf['aimleapTitle']+" "+deliDf['Weight_']+" "+deliDf['Count_']
deliDf['aimleapTitle'] = deliDf['aimleapTitle'].apply(lambda x:x.strip())
deliDf['aimleapTitle'] = deliDf['aimleapTitle'].apply(lambda x:getNewStr(x))
deliDf['aimleapTitle'] = deliDf['aimleapTitle'].apply(lambda x:cleanTitle(x).replace(" package",'').replace('|package',''))
deliDf = deliDf.rename(columns={"aimleapTitle":"NewTitle"})
deliDf = deliDf.reset_index(drop=True)
NewTitles = deliDf['NewTitle'].unique()
aimleapIds = ["Aimleap"+str(i) for i in range(len(NewTitles))]
aimleapIdsdf = pd.DataFrame(aimleapIds,columns=['aimleapId'])
NewTitlesdf = pd.DataFrame(NewTitles,columns=['title'])
NewTitlesdf['aimleapId'] = aimleapIdsdf['aimleapId']

deliDf['aimleapId'] = deliDf['NewTitle'].apply(lambda x:getAimleapId(x))
deliDf['source'] = deliDf['url'].apply(lambda x:x.split("/")[2])
deliDf['source'] = deliDf['source'].apply(lambda x:x.split(".")[1])
deliDf['newUpc'] = deliDf.apply(lambda x:x['source'][0]+str(x['upc']),axis=1)
deliDf['aimleapTitlewithsource'] = deliDf['product_title'] +" + "+ deliDf['source']

nationalBrand = deliDf[deliDf['brandStatus']=='national brand']
storeBrand = deliDf[deliDf['brandStatus']=='store brand']

nationalBrandgrupd1 = getCleannationalBrand(nationalBrand)
storeBrandgrupd1 = getCleanstoreBrand(storeBrand)

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
       'target_url', 'walmart_url', 'UPC','weight','aimleapTitlewithsource']]

# with pd.ExcelWriter("classification_deli_"+str(datetime.now().date())+".xlsx",engine='xlsxwriter',options={"strings_to_urls":False}) as writer:
#     storeBrandgrupd.to_excel(writer,index=False)

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
with pd.ExcelWriter("classification_deli_"+str(datetime.now().date())+".xlsx",engine='xlsxwriter',options={"strings_to_urls":False}) as writer:
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

    
with pd.ExcelWriter("deliProductMatching_"+str(datetime.now().date())+".xlsx",engine='xlsxwriter',options={"strings_to_urls":False}) as writer:
    productMtchingDf.to_excel(writer,index=False)

