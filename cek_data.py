import requests
import json

detail_url = 'https://gql.tokopedia.com/graphql/productReviewList'

payload_detail = [{
    'operationName': 'productReviewList',
    'query' : 'query productReviewList($productID: String!, $page: Int!, $limit: Int!, $sortBy: String, $filterBy: String) {\n  productrevGetProductReviewList(productID: $productID, page: $page, limit: $limit, sortBy: $sortBy, filterBy: $filterBy) {\n    productID\n    list {\n      id: feedbackID\n      variantName\n      message\n      productRating\n      reviewCreateTime\n      reviewCreateTimestamp\n      isReportable\n      isAnonymous\n      imageAttachments {\n        attachmentID\n        imageThumbnailUrl\n        imageUrl\n        __typename\n      }\n      videoAttachments {\n        attachmentID\n        videoUrl\n        __typename\n      }\n      reviewResponse {\n        message\n        createTime\n        __typename\n      }\n      user {\n        userID\n        fullName\n        image\n        url\n        __typename\n      }\n      likeDislike {\n        totalLike\n        likeStatus\n        __typename\n      }\n      stats {\n        key\n        formatted\n        count\n        __typename\n      }\n      badRatingReasonFmt\n      __typename\n    }\n    shop {\n      shopID\n      name\n      url\n      image\n      __typename\n    }\n    hasNext\n    totalReviews\n    __typename\n  }\n}\n',
    'variables': {
        'filterBy' : "",
        'limit' : 100,
        'page' : 1,
        'productID' : '5562379354',
        'sortBy' : "create_time desc"
    }
}]

req2 = requests.post(detail_url, json=payload_detail).json()
rows2 = req2[0]['data']['productrevGetProductReviewList']

print(rows2['list'][38]['user']['url'])