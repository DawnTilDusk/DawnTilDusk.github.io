#include <iostream>
#include <cstdio>
#include <cstring>
#include <cmath>
#include <algorithm>
using namespace std;
int a[6];

int main(){
	while(cin>>a[1]>>a[2]>>a[3]>>a[4]>>a[5]){
		bool flag = 0;
		for(int i=2; i<=5; i++)
			if(a[i] < a[i-1]) flag = 1;
		if(!flag){
			printf("Yes");
		}
		else{
			printf("No ");
			sort(a+1, a+6);
			for(int i=1; i<=5; i++)
				printf("%d ", a[i]);
		}
		printf("\n");
	}
	return 0;
}
