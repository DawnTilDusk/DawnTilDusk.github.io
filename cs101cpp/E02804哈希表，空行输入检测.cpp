#include <iostream>
#include <string>
#include <unordered_map>
using namespace std;

int main() {
    unordered_map<string, string> dictionary;
    string line;
    
    // ��ȡ�ʵ䲿��
    while (getline(cin, line) && !line.empty()) {
        size_t space_pos = line.find(' ');
        string english = line.substr(0, space_pos);
        string foreign = line.substr(space_pos + 1);
        dictionary[foreign] = english;
    }
    
    // ��ȡ��ѯ���ֲ�����
    string query;
    while (getline(cin, query)) {
        if (dictionary.find(query) != dictionary.end()) {
            cout << dictionary[query] << endl;
        } else {
            cout << "eh" << endl;
        }
    }
    
    return 0;
}
