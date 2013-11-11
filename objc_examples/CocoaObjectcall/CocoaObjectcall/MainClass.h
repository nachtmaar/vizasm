//
//  MainClass.h
//  CocoaObjectcall
//
//  Created by nils on 22.08.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import <Foundation/Foundation.h>

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

@interface MainClass : NSObject{
  Object1 *obj1;
  Object2 *obj2;
  Object3 *obj3;
  __unsafe_unretained NSString *command;
}
- (void)method1;
@property (strong, readwrite) Object1 *obj1;
@property (strong, readwrite) Object2 *obj2;
@property (strong, readwrite) Object3 *obj3;
@property (assign) NSString *command;

@end


class CPP{
public:
  int bar(int i1, int i2, int i3) {
    return i1 + i2 + i3;
  }
  int foo(int i1, int i2, int i3) {
    return bar(i1, i2, i3);
  }
};