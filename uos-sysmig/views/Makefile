.PHONY:clean
VPATH = math:.

#CC = gcc
#RM = rm
CFLAGS = -fPIC
CLIBS := -L/usr/lib64/mysql -lmysqlclient -lssh
OBJ = check_user_authority.c get_databese.c sql.c ssh_shell.c
OBJS = check_user_authority.o get_databese.o sql.o ssh_shell.o
TARGET = check_user_authority.so

$(TARGET) :$(OBJS)
	g$(CC) -shared $(CFLAGS) -o $@ $^ $(CLIBS)

$(OBJS) :$(OBJ)
	g$(CC) -c $(CFLAGS) $^

clean:
	$(RM) $(TARGET) $(OBJS)
