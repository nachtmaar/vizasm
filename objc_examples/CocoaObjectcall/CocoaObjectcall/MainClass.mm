//
//  MainClass.m
//  CocoaObjectcall
//
//  Created by nils on 22.08.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import "MainClass.h"
#import "StaticMethods.h"
#import "Subclass.h"

@implementation MainClass
@synthesize obj1, obj2, obj3, command;

// instance variable test method
- (void)instanceVars{
  obj1 = [[Object1 alloc] init];
  [obj1 printObject1];
  obj2 = [[Object2 alloc] init] ;
  [obj2 printObject];
  obj3 = [[Object3 alloc] init];
  [obj1 printObject];
  [obj2 printObject2];
  [obj3 printObject3];
  [self cppMethodCall];
}
- (void)cppMethodCall{
  CPP cpp;
  cpp.foo(1,2,3);
}



- (void)method1{
  [self floatMethod:1.0 f2:2.0 str:@"" f3:3.0];
  NSLog(@"%d%d%d%d%d%d%d%d%d", 1,2,3,4,5,6,7,8,9);
  [self selfMethod:@"selfmethod1"];
  obj1 = [[Object1 alloc] init];
  [obj1 longSelector:@"1" str2:@"2" str3:@"3" str4:@"4" str5:@"5" str6:@"6"];
  [obj1 longSelector:@"1" str2:@"2" str3:@"3" str4:@"4" str5:@"5" str6:@"6"];
  obj1->obj1_int = 5;
  [obj1 printObject1];
  obj2 = [[Object2 alloc] init] ;
  [self selfMethod:@"selfmethod2"];
  [obj2 printObject];
  obj3 = [[Object3 alloc] init];
  NSLog(@"nslog statement without var");
  [obj3 printObject];
  [StaticMethods staticPrint];
  [obj1 printObject];
  [obj2 printObject2];
  [obj3 printObject3];
  NSString *msg = @"nslog msg from variable";
  NSLog(@"%@", msg);
  [obj3 printObject3];
  [self selfMethod:@"selfmethod3"];
  NSUserDefaults *def =[NSUserDefaults standardUserDefaults];
  [def setObject:@"" forKey:@"aKey"];
  //self.command = @"self notation";
  command = @"dot notation";
  NSLog(@"%d", 5);
  [[NSUserDefaults standardUserDefaults] objectForKey:@"defaults"];
  NSURL *url = [NSURL URLWithString:@""];
  NSArray *arr = [NSArray arrayWithObject:@"12"];
  [self longMethod:@"" long2:@""];
  [[Subclass alloc] init];
}

- (void)selfMethod:(NSString*)arg1{
  int cnt = 5;
  cnt++;
  id obj = [[NSUserDefaults standardUserDefaults] objectForKey:@"aKey"];
  [obj main];
}

- (void)longMethod:(NSString *)str1 long2:(NSString*)str2{
  id selfref = self;
  [self selfMethod:@"selfmethod1"];
  NSLog(@"%s", _cmd);
  [str1 UTF8String];
  [str2 UTF8String];
  self.command = str1;
}

- (void)floatMethod:(float)f f2:(float)f2 str:(NSString*)str f3:(float)f3{
  
}

- (CGRect)fpretMsgSend{
  CGRect rect = CGRectMake(0, 0, 255, 255);
#if TARGET_OS_IPHONE
  rect = [UIScreen mainScreen].bounds;
#endif //TARGET_OS_IPHONE
  [self fpretReceiver:@"string" fpretReceiver:rect];
  return rect;
}
- (void)fpretReceiver:(NSString *)str fpretReceiver:(CGRect)rect {
  
}

@end

@implementation SuperObject

- (void)printObject{
  NSLog(@"I am: %@", self.class);
}

@end

@implementation Object1
- (void)printObject1{
  NSLog(@"I am: %@", self.class);
  [self self];
  NSString *foo = @"foo";
  [self longSelector:foo str2:foo str3:foo str4:foo str5:foo str6:foo];
}

void cFunction(int i1, int i2, int i3) {
  if(i1 == 0) return;
  cFunction(0, i1, i2);
  printf("%d%d%d", i1, i2, i3);
  
}

- (void)longSelector:(NSString *)str1 str2:(NSString*)str2 str3:(NSString *)str3 str4:(NSString *)str4 str5:(NSString *)str5 str6:(NSString *)str6{
  [self printObject1];
  NSLog(@"%@", _cmd);
  str1 = [str1 stringByAppendingString:@"foo1"];
  str2 = [str2 stringByAppendingString:@"foo2"];
  str3 = [str3 stringByAppendingString:@"foo3"];
  str4 = [str4 stringByAppendingString:@"foo4"];
  str5 = [str5 stringByAppendingString:@"foo5"];
  str6 = [str6 stringByAppendingString:@"foo6"];
  [str3 UTF8String];
  [str4 UTF8String];
  [str5 UTF8String];
  [str6 UTF8String];
  NSString *str11 = @"foo11";
  NSString *str12 = @"foo12";
  NSString *str13 = @"foo13";
  NSString *str14 = @"foo14";
  NSString *str15 = @"foo15";
  NSString *str16 = @"foo16";
  NSLog(@"%@", str3);
  NSLog(@"%@", str13);
  NSLog(@"%@", str6);
  NSLog(@"%@", str14);
  NSLog(@"%@", str12);
  NSLog(@"%@", str11);
}
@end
@implementation Object2
- (void)printObject2{
  [self hash];
  NSLog(@"I am: %@", self.class);
}
@end

@implementation Object3
- (void)printObject3{
  [self copy];
  NSLog(@"I am: %@", self.class);
  cFunction(1, "cstring", 2, "cstring2", "cstring3", "cstring4", "cstring5", "cstring6");
}

void cFunction(int i1, char *str, int i2, char *str2, char *str3, char *str4, char *str5, char *str6) {
  printf("%d, %s, %d, %s, %s, %s, %s, %s", i1, str, i2, str2, str3, str4, str5, str6);
}
@end

