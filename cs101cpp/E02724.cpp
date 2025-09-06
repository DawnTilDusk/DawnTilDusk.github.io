#include <iostream>
#include <cstdio>
#include <cstring>
#include <queue>

using namespace std;

struct stu{
	char num[20];
	int m, d;
};

stu list[100001];
queue<stu> ans[13][32];

bool equal(stu s1, stu s2){
	return s1.m == s2.m && s1.d == s2.d;
}

void emptyQueue(queue<stu> s){
	while(!s.empty()){
		printf("%s ", s.front().num);
		s.pop();
	}
}

int main(){
	int n;
	scanf("%d", &n);
	for(int i=1; i<=n; i++){
		scanf("%s %d %d", &list[i].num, &list[i].m, &list[i].d);
		for(int j=1; j<i; j++)
			if(equal(list[i], list[j])){
				if(ans[list[i].m][list[i].d].empty())
					ans[list[i].m][list[i].d].push(list[j]);
				ans[list[i].m][list[i].d].push(list[i]);
				break;
			}
	}
	for(int i=1; i<=12; i++)
		for(int j=1; j<=31; j++)
			if(!ans[i][j].empty()){
				printf("%d %d ", i, j);
				emptyQueue(ans[i][j]);
				printf("\n");
			}			
	return 0;
}
