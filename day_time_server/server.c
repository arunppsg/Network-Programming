/*
 * Day time server
 */

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <time.h>

#define LISTENQ 5
#define MAXLINE 100

int main(int argc, char* argv[]){
    int err;
    int listenfd, connfd;
    struct sockaddr_in servaddr;
    char buff[MAXLINE];
    time_t ticks;

    listenfd = socket(AF_INET, SOCK_STREAM, 0);
    
    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    servaddr.sin_port = htons(8899);

    err = bind(listenfd, (struct sockaddr*) &servaddr, sizeof(servaddr));
    if(err < 0){
        printf("Error binding to socket\n");
    }
    listen(listenfd, LISTENQ);

    while(1){
        connfd = accept(listenfd, (struct sockaddr*)NULL, NULL);
        ticks = time(NULL);
        snprintf(buff, sizeof(buff), "%.24s\r\n", ctime(&ticks));
        write(connfd, buff, strlen(buff));
    }
    return 0;
}
