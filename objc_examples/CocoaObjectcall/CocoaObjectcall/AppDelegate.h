//
//  AppDelegate.h
//  CocoaObjectcall
//
//  Created by nils on 27.02.13.
//  Copyright (c) 2013 nils. All rights reserved.
//
// The following source code has been written to see how it gets translated to assembler code.
// The source is not written very good nor does it have any semantic meaning.
// It think it doesn't even run. So do not complain!
// Just compile it and throw it into Hopper if you want


#import <Cocoa/Cocoa.h>

@interface SuperObject : NSObject
- (void)printObject;
@end

@interface Object1 : SuperObject{
    @public int obj1_int;
}

- (void)printObject1;
- (void)longSelector:(NSString *)str1 str2:(NSString*)str2 str3:(NSString *)str3 str4:(NSString *)str4 str5:(NSString *)str5 str6:(NSString *)str6;
@end

@interface Object2 : SuperObject
- (void)printObject2;
@end

@interface Object3 : SuperObject
- (void)printObject3;
@end

@interface AppDelegate : NSObject <NSApplicationDelegate>{
}

- (void)selfMethod:(NSString*)arg1;

@property (assign) IBOutlet NSWindow *window;



@end



