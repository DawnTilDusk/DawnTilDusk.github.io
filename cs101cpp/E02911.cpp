#include <iostream>
#include <cstdio>
#include <cstring>
#include <cmath>
#include <algorithm>
#include <set>
using namespace std;

bool check(int a, int b){
	for(int i=1; i<=9; i++)
		if(a - b == i*1000+i*100+i*10+i)
			return 1;
	return 0;
}

set<int> s;
set<int>::iterator it;

int main(){
	int m, cap;
	scanf("%d", &m);
	cap = sqrt(m);
	for(int i=32; i<=cap; i++)
		for(int j=i; j<=cap; j++)
			if(check(j*j, i*i))
				s.insert(j*j);
	for(it = s.begin(); it != s.end(); it++)
		printf("%d\n", *it);
	return 0;
}
