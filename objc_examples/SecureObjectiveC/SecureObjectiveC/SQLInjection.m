// Schocken

// Created by nils on 15.04.13.
//
//


#import "SQLInjection.h"

@implementation SQLInjection {

}
- (id)init {
	self = [super init];
	if (self) {

	}

	return self;
}

/*
source:
http://www.techotopia.com/index.php/An_Example_SQLite_based_iOS_4_iPhone_Application
http://stackoverflow.com/questions/7622610/libsqlite-in-simulator-and-ios-compiling/7623043#7623043
 http://stackoverflow.com/questions/17592844/how-to-save-the-data-in-sqlite3-in-iphone
 */
- (void)sqlInjection{

  // open db
  sqlite3 *db = [self openDb];
  
  // prep statement
  sqlite3_stmt    *statement;
  NSString *querySQL = @"update contacts set name=?,address=?,phone=? where id=?";
  NSLog(@"query: %@", querySQL);
  const char *query_stmt = [querySQL UTF8String];
  
  const char *name =[@"Max Mustermann" UTF8String];
  const char *addr = [@"Musterhausen"  UTF8String];
  const char *tele =[@"Mustertelenr" UTF8String];
  long idNr = 1L;
  
  // preparing a query compiles the query so it can be re-used.
  sqlite3_prepare_v2(db, query_stmt, -1, &statement, NULL);
  sqlite3_bind_text(statement, 1, name, -1, SQLITE_STATIC);
  sqlite3_bind_text(statement, 2, addr, -1, SQLITE_STATIC);
  sqlite3_bind_text(statement, 3, tele, -1, SQLITE_STATIC);
  sqlite3_bind_int64(statement, 4, idNr);
  
  // process result
  if (sqlite3_step(statement) != SQLITE_DONE)
  {
    printf("error: %s", sqlite3_errmsg(db));
  }
  
  sqlite3_finalize(statement);
  
  // exploitable way
  NSString *querySQL2 = [NSString stringWithFormat:@"update contacts set name=%@,address=%@,phone=%@ where id=%l", name, addr, tele, idNr];
  sqlite3_prepare_v2(db, [querySQL2 UTF8String], -1, &statement, NULL);
  
  // process result
  if (sqlite3_step(statement) != SQLITE_DONE)
  {
    printf("error: %s", sqlite3_errmsg(db));
  }
  
  sqlite3_finalize(statement);
  
  c_method_with_args(5);
  c_method_without_args();
  c_method_with_args(5);
  c_method_without_args();
}

void c_method_without_args(void) {
  printf("foo");
  return;
}

void c_method_with_args(int i) {
  printf("foo %d", i);
  return;
}

- (sqlite3 *)openDb{
	sqlite3 *db;

	NSArray *dirPaths =  NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
	NSString *docsDir = [dirPaths objectAtIndex:0];
	NSString *databasePath = [[NSString alloc] initWithString: [docsDir stringByAppendingPathComponent: @"contacts.db"]];

	NSFileManager *filemgr = [NSFileManager defaultManager];

	if ([filemgr fileExistsAtPath: databasePath ] == NO)
	{
		const char *dbpath = [databasePath UTF8String];

		if (sqlite3_open(dbpath, &db) == SQLITE_OK)	{
			char *errMsg;
			const char *sql_stmt = "CREATE TABLE IF NOT EXISTS CONTACTS (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT, ADDRESS TEXT, PHONE TEXT)";

			if (sqlite3_exec(db, sql_stmt, NULL, NULL, &errMsg) != SQLITE_OK) {
				printf("%s", "Failed to create table");
			}
			sqlite3_close(db);
		}
		else {
			printf("%s", "Failed to open/create database");
		}
	}
	return db;
}

@end