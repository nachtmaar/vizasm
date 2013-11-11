//
//  CarrierStuff.m
//  SecureObjectiveC
//
//  Created by nils on 16.09.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import "CarrierStuff.h"
#import <CoreTelephony/CTTelephonyNetworkInfo.h>
#import <CoreTelephony/CTCarrier.h>

@implementation CarrierStuff

 //TODO: of any interest??
// Source :http://stackoverflow.com/questions/3043335/determine-iphone-users-country
+ (void)carrierStuff{
  CTTelephonyNetworkInfo *netInfo = [[CTTelephonyNetworkInfo alloc] init];
  CTCarrier *carrier = [netInfo subscriberCellularProvider];
  NSString *mcc = [carrier mobileCountryCode];
  NSString *mnc = [carrier mobileNetworkCode];
  NSLog(@"country code: %@, network code: %@", mcc, mnc);
}


@end
