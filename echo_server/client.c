#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define MAXLINE 1000
#define LISTENQ 20

void str_cli(int sockfd){
    /* The lines in the file are sent to the server.
     * Ther server echoes the lines back to the client */
    int len = 100;
    char sendline[MAXLINE], recvline[MAXLINE];
    FILE* fp = fopen("file.txt", "r"); 
    while(fgets(sendline, 100, fp)){
        write(sockfd, sendline, strlen(sendline));
        printf("Read line %s", sendline);
        if (read(sockfd, recvline, MAXLINE)){
            printf("Received line: %s", recvline);
        }
    }
    fclose(fp);
}

int main(){
    int sockfd;
    struct sockaddr_in servaddr;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    servaddr.sin_port = htons(8800);

    if(connect(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr)) == 0){
        printf("Connect success\n");
    } else {
        printf("Connect failed ");
        return 0;
    }
    str_cli(sockfd);
    close(sockfd);
    return 0;
}
