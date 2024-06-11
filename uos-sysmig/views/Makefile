.PHONY:clean
VPATH = math:.

#CC = gcc
#RM = rm
CFLAGS = -fPIC
CLIBS := -L/usr/lib64/mysql -lmysqlclient
OBJ = check_user_authority.c
OBJS = check_user_authority.o
TARGET = check_user_authority.so

$(TARGET) :$(OBJS)
	g$(CC) -shared -o $@ $^ $(CLIBS)

$(OBJS) :$(OBJ)
	g$(CC) -c $(CFLAGS) $^ -o $@ $(CLIBS)

clean:
	$(RM) $(TARGET) $(OBJS)
