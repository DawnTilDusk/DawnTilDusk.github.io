#include <iostream>
#include <cstdio>
#include <cstring>

using namespace std;

int main(){
	int n;
	scanf("%d", &n);
	if(n%2){
		printf("0 0");
		return 0;
	}
	int min = n/4 + (n%4)/2;
	int max = n/2;
	printf("%d %d", min, max);
	return 0;
}
