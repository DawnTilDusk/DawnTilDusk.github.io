#include <iostream>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <cstring>

using namespace std;
int pri[300];
bool notPrime[3000];

int init(int n){
	int cnt = 0;
	for(int i=2; i<=n; i++){
		if(!notPrime[i])
			pri[++cnt] = i;
		for(int j=1; j<=cnt; j++){
//			cout << i << " " << j << " " << pri[j]<< endl;
			if(i * pri[j] > n) break;
			notPrime[i * pri[j]] = true;
			if(i % pri[j] == 0) break;
		}
	}
	return cnt;
}

int main(){
	int x;
	scanf("%d", &x);
	if(x < 6 || x%2 != 0){
		printf("Error!");
		return 0;
	}
	int cnt = init(x);
	for(int i=1; i<=cnt; i++)
		for(int j=i; j<=cnt; j++)
			if(pri[i] + pri[j] == x)
				printf("%d=%d+%d\n", x, pri[i], pri[j]);
	return 0;
}
