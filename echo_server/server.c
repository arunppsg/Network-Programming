#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define MAXLINE 1000
#define LISTENQ 20

void str_echo(int sockfd){
    /* Reads from a socket
     * and write backs to the same socket */
    int n;
    char buf[MAXLINE];
    memset(&buf, 0, MAXLINE);
    while((n = recv(sockfd, buf, MAXLINE, 0)) > 0){
        printf("Received line: %s", buf);
        send(sockfd, buf, MAXLINE, 0);
    } 
}

int main(){
    int err;
    int listenfd, connfd;
    struct sockaddr_in servaddr, cliaddr;
    socklen_t clilen;

    listenfd = socket(AF_INET, SOCK_STREAM, 0);

    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    servaddr.sin_port = htons(8800);
    
    err = bind(listenfd, (struct sockaddr*)&servaddr, sizeof(servaddr));
    if(err == 0){
        printf("Successfuly binded port\n");
    } else {
        printf("Bind failure\n");
        return 0;
    }

    err = listen(listenfd, LISTENQ);
    if(err == 0){
        printf("Listen success\n");
    } else {
        printf("Listen failed\n");
        return 0;
    }

    while(1){
        /* Accept connections, echo results */
        clilen = sizeof(cliaddr);
        connfd = accept(listenfd, (struct sockaddr*)&cliaddr, &clilen);
        str_echo(connfd);
        close(connfd);
    }
    return 0;
}
