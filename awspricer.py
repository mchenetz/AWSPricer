import requests
import sys
import json
import os


class awspricer:

    def __init__(self, region):
        print('AWSPricer API Michael Chenetz 2017')
        self.allProducts = []
        self.allPricing = []
        self.allProductIds = []
        self.allPricingIds = []
        self.regionMap = {
            'us-east-1': 'US East (N. Virginia)',
            'us-east-2': 'US East (Ohio)',
            'us-west-1': 'US West (N. California)',
            'us-west-2': 'US West (Oregon)'
        }
        self.productKeyMap = ['instanceType','vcpu','memory','operatingSystem']
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.ec2pricingpath = os.path.join(self.dir_path, 'ec2pricing')
        if region in self.regionMap.keys():
            self.region = region
            self.ec2 = self.loadpricing()
            self.ec2products = self.ec2['products']
            self.ec2pricing = self.ec2['terms']

        else:
            print('You must define a valid region')
            sys.exit(1)

    def getlatestpricing(self):
        print(self.dir_path)
        response = requests.get('https://pricing.{region}.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json'
                                .format(region=self.region))
        with open(os.path.join(self.ec2pricingpath, 'index.json'),'w+') as out:
            json.dump(response.json(), out)
            out.flush()
            out.close()
        response.close()
        return 0



    def loadpricing(self):
        if os.path.exists(os.path.join(self.ec2pricingpath, 'index.json')):
            response = open('ec2pricing/index.json')
            ec2pricing = json.load(response)
            response.close()
            return ec2pricing


    def filterproducts(self, **kwargs):
        products = self.ec2products
        for key, value in kwargs.items():
            ## Remove already filtered items from Products
            if self.allProductIds:
                for id in products.copy():
                    if id not in self.allProductIds:
                        del products[id]
                self.allProductIds=[]
            for id in products:
                    for attributes in products[id]['attributes']:
                            # vcpu, memory
                            if key == attributes:
                                if str(value) == str(products[id]['attributes'][key]):
                                    self.allProductIds.append(id)
        return self

    def filterprice(self, **kwargs):
        productIds = self.allProductIds
        pricing = self.ec2pricing
        for key, value in kwargs.items():
            for type in pricing:
                for id in pricing[type]:
                    for offer in pricing[type][id]:
                        for attributes in pricing[type][id][offer]['termAttributes']:
                            if key == attributes:
                                if str(value) == pricing[type][id][offer]['termAttributes'][attributes]:
                                    if productIds:
                                        if id in productIds:
                                            self.allPricingIds.append(offer)
                                    else:
                                        self.allPricingIds.append(offer)
        return self

    def getproducts(self):
        products = self.ec2products
        filteredids = self.allProductIds
        for id in products:
            if filteredids:
                if id in filteredids:
                    self.allProducts.append(products[id])
                else:
                    self.allProducts.append(products[id])
        return self.allProducts

    def getprice(self):
        pricing = self.ec2pricing
        filteredids = self.allProductIds
        filteredpricing = self.allPricingIds
        for type in pricing:
            for id in pricing[type]:
                for offer in pricing[type][id]:
                    if filteredpricing:
                        if offer in filteredpricing:
                            self.allPricing.append(pricing[type][id][offer])
                    elif filteredids and not filteredpricing:
                        if id in filteredids:
                            self.allPricing.append(pricing[type][id][offer])
                    else:
                        self.allPricing.append(pricing[type][id][offer])
        return self.allPricing


if __name__ == '__main__':
    pricer = awspricer('us-east-1')

    products = pricer.filterproducts(vcpu='4', memory='16 GiB').filterprice(PurchaseOption='No Upfront').getprice()
    print (products)
