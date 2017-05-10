import requests
import sys
import json
import os

class awspricer:

    def __init__(self, region):
        self.regionMap = {
            'us-east-1': 'US East (N. Virginia)',
            'us-east-2': 'US East (Ohio)',
            'us-west-1': 'US West (N. California)',
            'us-west-2': 'US West (Oregon)'
        }
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
        response = requests.get('https://pricing.{region}.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json'.format(region=self.region))
        with open(os.path.join(self.ec2pricingpath, 'index.json'),'w+') as out:
            json.dump(response.json(), out)
            out.flush()
            out.close()
        response.close()
        return 0

    def getproductsbyos(self,os,filterset=[]):
        allProducts = []
        if filterset != []:
            products = {item['sku']:item for item in filterset}
        else:
            products = self.ec2products
        for id in products:
            att = products[id]['attributes']
            family = products[id]['productFamily']
            if family=='Compute Instance':
                if att['operatingSystem']==os:
                    allProducts.append(products[id])
        return allProducts

    def getproductsbyregion(self, region, filterset=[]):
        allProducts = []
        if filterset != []:
            for list in filterset:
                products = {item['sku']:item for item in filterset}
        else:
            products = self.ec2products
        for id in products:
            att = products[id]['attributes']
            family = products[id]['productFamily']
            if family == 'Compute Instance':
                if att['location']==self.regionMap[region]:
                    allProducts.append(products[id])
        return allProducts


    def loadpricing(self):
        if os.path.exists(os.path.join(self.ec2pricingpath, 'index.json')):
            response = open('ec2pricing/index.json')
            ec2pricing = json.load(response)
            response.close()
            return ec2pricing


    def price(self, size):
        ec2products = self.ec2products
        ec2pricing = self.ec2pricing
        vcpu = ''
        mem = ''
        instanceType = ''
        for id in ec2products:
            if len(id) == 16:
                family = ec2products[id]['productFamily']
                if 'vcpu' in ec2products[id]['attributes'].keys():
                    vcpu = ec2products[id]['attributes']['vcpu']
                if 'memory'in ec2products[id]['attributes'].keys():
                    mem = ec2products[id]['attributes']['memory']
                if 'instanceType' in ec2products[id]['attributes'].keys():
                    instanceType = ec2products[id]['attributes']['instanceType']
                if family == 'Compute Instance':
                    print (id + ': ' + family)
                    print ('VCPU: ' + vcpu)
                    print ('Memory: ' + mem)
                    print ('Instance Type: ' + instanceType)
            onDemand = ec2pricing['OnDemand'][id]
            for priceId in onDemand:
                if 'offeringClass' not in onDemand[priceId]['termAttributes'].keys():
                    priceDimensions = onDemand[priceId]['priceDimensions']
                    for costId in priceDimensions:
                        print('units: ' + str(priceDimensions[costId]['unit']))
                        if priceDimensions[costId]['unit']=='Hrs':
                            print('Cost Per/Hr: ' + str(priceDimensions[costId]['pricePerUnit']['USD']))

if __name__ == '__main__':
    print('Main')
    pricer = awspricer('us-east-1')
    # linux = pricer.getproductsbyos('Linux')
    # pricing = pricer.ec2pricing
    # for sku in linux:
    #     print (sku['sku'] + ':')
    #     att = sku['attributes']
    #     print ('Operating System : ' + att['operatingSystem'])
    #     print ('License Model    : ' + att['licenseModel'])
    #     print ('Virtual CPUs     : ' + str(att['vcpu']))
    #     print ('Instance Model   : ' + att['instanceType'])
    #     print ('Memory           : ' + str(att['memory']))
    #     instPrice = pricing['OnDemand'][sku['sku']]
    #     for price in instPrice:
    #         pd = instPrice[price]['priceDimensions']
    #         for pricedim in pd:
    #             print ('Price/hr         : ' + str(pd[pricedim]['pricePerUnit']['USD']))
    for price in pricer.getproductsbyos('Linux',pricer.getproductsbyregion('us-east-1')):
        print(price['attributes']['operatingSystem'])
        print(price['attributes']['location'])

    #print(pricer.getlatestpricing())
    #print(pricer.price('hello'))
