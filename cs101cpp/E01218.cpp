#include <cstdio>
#include <iostream>
using namespace std;
bool door[1000001];
int main(){
    int m, n;
    scanf("%d", &m);
    for (int l = 1; l <= m; l++) {
		scanf("%d", &n);
    	for(int i=1; i<=n;i++){
    		door[i] = 0;
		}
        for(int i = 1; i<= n; i++){
            for(int j = i; j <= n; j += i){
                door[j] = !door[j];
            }
/*	      	for(int i = 1; i<=n; i++){
 	  			cout << door[i]<<" ";
    		}
    		cout << endl;*/
        }
	    int cnt = 0;
    	for(int i = 1; i<=n; i++){
//    		cout << door[i]<<" ";
    	    cnt += door[i];
    	}
    	printf("%d\n", cnt);
    }
    return 0;
}

