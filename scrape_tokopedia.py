import requests
import json
import pandas as pd
from os.path import exists
import time

start_time = time.time()
cari = [
    'oppo f5',
    'xiaomi'
]
url = 'https://gql.tokopedia.com/graphql/SearchProductQueryV4'
detail_url = 'https://gql.tokopedia.com/graphql/productReviewList'

def getParam():
    params = []
    for i in range(0, len(cari)):
        for j in range(1, 101):
            param = 'device=desktop&navsource=&ob=23&page={}&q={}&related=true&rows=60&safe_search=false&scheme=https&shipping=&source=search&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=product&start={}&topads_bucket=true&unique_id=f7d9d4a5e482e96916f28ce6a66b8eb2&user_addressId=193933254&user_cityId=298&user_districtId=4030&user_id=15252766&user_lat=-1.8806991&user_long=109.9767669&user_postCode=78822&user_warehouseId=0&variants='.format(j, cari[i], (j-1)*60)
            params.append(param)

    return params


def getPayload(param):
    payload = [{
        'operationName': 'SearchProductQueryV4',
        'variables': {
            'params': param
        },
        'query' : "query SearchProductQueryV4($params: String!) {\n  ace_search_product_v4(params: $params) {\n    header {\n      totalData\n      totalDataText\n      processTime\n      responseCode\n      errorMessage\n      additionalParams\n      keywordProcess\n      componentId\n      __typename\n    }\n    data {\n      banner {\n        position\n        text\n        imageUrl\n        url\n        componentId\n        trackingOption\n        __typename\n      }\n      backendFilters\n      isQuerySafe\n      ticker {\n        text\n        query\n        typeId\n        componentId\n        trackingOption\n        __typename\n      }\n      redirection {\n        redirectUrl\n        departmentId\n        __typename\n      }\n      related {\n        position\n        trackingOption\n        relatedKeyword\n        otherRelated {\n          keyword\n          url\n          product {\n            id\n            name\n            price\n            imageUrl\n            rating\n            countReview\n            url\n            priceStr\n            wishlist\n            shop {\n              city\n              isOfficial\n              isPowerBadge\n              __typename\n            }\n            ads {\n              adsId: id\n              productClickUrl\n              productWishlistUrl\n              shopClickUrl\n              productViewUrl\n              __typename\n            }\n            badges {\n              title\n              imageUrl\n              show\n              __typename\n            }\n            ratingAverage\n            labelGroups {\n              position\n              type\n              title\n              url\n              __typename\n            }\n            componentId\n            __typename\n          }\n          componentId\n          __typename\n        }\n        __typename\n      }\n      suggestion {\n        currentKeyword\n        suggestion\n        suggestionCount\n        instead\n        insteadCount\n        query\n        text\n        componentId\n        trackingOption\n        __typename\n      }\n      products {\n        id\n        name\n        ads {\n          adsId: id\n          productClickUrl\n          productWishlistUrl\n          productViewUrl\n          __typename\n        }\n        badges {\n          title\n          imageUrl\n          show\n          __typename\n        }\n        category: departmentId\n        categoryBreadcrumb\n        categoryId\n        categoryName\n        countReview\n        customVideoURL\n        discountPercentage\n        gaKey\n        imageUrl\n        labelGroups {\n          position\n          title\n          type\n          url\n          __typename\n        }\n        originalPrice\n        price\n        priceRange\n        rating\n        ratingAverage\n        shop {\n          shopId: id\n          name\n          url\n          city\n          isOfficial\n          isPowerBadge\n          __typename\n        }\n        url\n        wishlist\n        sourceEngine: source_engine\n        __typename\n      }\n      violation {\n        headerText\n        descriptionText\n        imageURL\n        ctaURL\n        ctaApplink\n        buttonText\n        buttonType\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }]

    return payload


def scrapeData(payload):
    product_id = ''
    id = ''
    nama_produk = ''
    review = ''
    rating = ''
    ctime = '' 
    author_username = ''
    shop_id = '' 
    anonymous = ''
    user_id  = ''
    req = requests.post(url, json=payload).json()
    rows = req[0]['data']['ace_search_product_v4']['data']['products']
    data_rows = []
    for i in range(0, len(rows)):
        product_id = rows[i]['id']
        payload_detail = [{
            'operationName': 'productReviewList',
            'query' : 'query productReviewList($productID: String!, $page: Int!, $limit: Int!, $sortBy: String, $filterBy: String) {\n  productrevGetProductReviewList(productID: $productID, page: $page, limit: $limit, sortBy: $sortBy, filterBy: $filterBy) {\n    productID\n    list {\n      id: feedbackID\n      variantName\n      message\n      productRating\n      reviewCreateTime\n      reviewCreateTimestamp\n      isReportable\n      isAnonymous\n      imageAttachments {\n        attachmentID\n        imageThumbnailUrl\n        imageUrl\n        __typename\n      }\n      videoAttachments {\n        attachmentID\n        videoUrl\n        __typename\n      }\n      reviewResponse {\n        message\n        createTime\n        __typename\n      }\n      user {\n        userID\n        fullName\n        image\n        url\n        __typename\n      }\n      likeDislike {\n        totalLike\n        likeStatus\n        __typename\n      }\n      stats {\n        key\n        formatted\n        count\n        __typename\n      }\n      badRatingReasonFmt\n      __typename\n    }\n    shop {\n      shopID\n      name\n      url\n      image\n      __typename\n    }\n    hasNext\n    totalReviews\n    __typename\n  }\n}\n',
            'variables': {
                'filterBy' : "",
                'limit' : 100,
                'page' : 1,
                'productID' : '{}'.format(product_id),
                'sortBy' : "create_time desc"
            }
        }]
        req2 = requests.post(detail_url, json=payload_detail).json()
        rows2 = req2[0]['data']['productrevGetProductReviewList']

        if len(rows2['list']) == 0:
                id = float('NaN')
                review = float('NaN')
                rating = float('NaN')
                ctime = float('NaN')
                author_username = float('NaN')
                anonymous = float('NaN')
                user_id = float('NaN')
                shop_id = float('NaN')
                nama_produk = float('NaN')

                data_rows.append(
                    (
                        product_id, 
                        nama_produk, 
                        review, 
                        rating, 
                        ctime, 
                        author_username, 
                        shop_id, 
                        anonymous, 
                        user_id, 
                        id
                    )
                )
        else:
            for j in range(0, len(rows2['list'])):
            
                id = rows2['list'][j]['id']
                review = rows2['list'][j]['message']
                rating = rows2['list'][j]['productRating']
                ctime = rows2['list'][j]['reviewCreateTime']
                author_username = rows2['list'][j]['user']['fullName']
                anonymous = rows2['list'][j]['isAnonymous']
                user_id = rows2['list'][j]['user']['userID']
                shop_id = rows2['shop']['shopID']
                nama_produk = rows[i]['name']

                data_rows.append(
                    (
                        product_id, 
                        nama_produk, 
                        review, 
                        rating, 
                        ctime, 
                        author_username, 
                        shop_id, 
                        anonymous, 
                        user_id, 
                        id
                    )
                )


    return data_rows


def importToCSV():
    df = pd.DataFrame(
        all_data, 
        columns=[
            'product_id', 
            'nama_produk', 
            'review', 
            'rating', 
            'ctime', 
            'author_username', 
            'shop_id',
            'anonymous',
            'user_id',
            'id'
            ])

    print(df)

    file_exist = exists('hasil\scrape_tokopedia.csv')

    if file_exist:
        df.to_csv('hasil\scrape_tokopedia.csv', mode='a', header=False, index=False)
    else:
        df.to_csv('hasil\scrape_tokopedia.csv', index=False)

    print('\nData Telah Tersimpan')
    print("\n--- {} minutes ---".format(((time.time() - start_time)/60)))


if __name__ == '__main__':
    params = getParam()
    all_data = []
    for i in range(0, len(params)):
        param = params[i]
        urls = getPayload(param)
        data = scrapeData(urls)
        all_data.extend(data)

    importToCSV()