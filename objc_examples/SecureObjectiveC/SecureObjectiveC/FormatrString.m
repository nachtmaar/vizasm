//
//  FormatrString.m
//  SecureObjectiveC
//
//  Created by nils on 17.04.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import "FormatrString.h"
#import "Entropy.h"

@implementation FormatrString

- (void)formatString:(NSString *)str{
  NSLog(@"%@", @"foo");
  [NSException exceptionWithName:@"name" reason:@"reason" userInfo:[NSDictionary dictionary]];
  NSString *str1 = [NSString stringWithFormat:@"%@", @"stringWithFormat"];
  NSLog(@"%@%@%@%@%@%@%@%@", @"1", @"2", @"3", @"4", @"5", @"6", @"7", @"8");
  NSLog(@"%@", str1);
  

  // TODO: ADD MORE EXAMPLES! AND C EXAMPLES!
  NSString *exploitableString = [NSString stringWithFormat:@"%@", @"foo"];
  NSLog(exploitableString);
  
  char foo[10];
  printf(foo);
  NSLog(str);
  
  char **foo2;
  initString(foo2);
  printf(foo2);
  
  char word[30];
  sprintf(word,foo, 1);
  
  [[[Entropy alloc] init] entropy];
}

void initString(char **str) {
  str = malloc(sizeof(char*) * 2);
  strcpy(str[0], "%s");
  strcpy(str[1], "foo");
}
@end
