#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define MAXLINE 100

int main(){
    int err;
    int sockfd, n;
    struct sockaddr_in servaddr;
    char buff[MAXLINE+1];

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    servaddr.sin_port = htons(8899);

    err = connect(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr));
    if(err < 0){
        printf("Error in connecting to socket ");
    }

    while((n = read(sockfd, buff, MAXLINE)) > 0){
        buff[n] = '\0';
        printf("Received: %s", buff);
    }
    return 0; 
}
