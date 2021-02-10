/*
Levenshtein distance: The admissible basic operations are 
insert, delete, and replace.
(Edit distance usually refers to Levenshtein distance)
I edit my code 
*/
#include <iostream>
#include <string>
#include <vector>
#define min3(a,b,c) min(a,min(b,c))
using namespace std;


int main() { 
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    string a, b;
    cin >> a >> b;
    a = " " + a;
    b = " " + b;
    
    int dp[a.size()][b.size()];
    memset(dp, 0, sizeof dp);
    for (int i = 1; i < a.size(); i++)
        dp[i][0]=i;
    for (int i = 1; i < b.size(); i++)
        dp[0][i]=i;
    for (int i = 1; i < a.size(); i++)
        for (int j = 1; j < b.size(); j++) {
            dp[i][j] = min3(dp[i-1][j] + 1, dp[i][j-1] + 1,(a[i]!=b[j]) + dp[i-1][j-1]);
            if(i>1 && j>1 && a[i]==b[j-1] && a[i-1]==b[j]) 
                dp[i][j] = min(dp[i][j], dp[i-2][j-2] + 1);
        }
    
    cout << "Total number of moves: " << dp[a.size()-1][b.size()-1] << endl << endl;
    
    for (int i = 1; i < a.size(); i++, cout << endl)
        for (int j = 1; j < b.size(); j++)
            cout << dp[i][j] << " ";
    cout << endl;
    

    cout << "MOVES: "<< endl;
    int n=a.size()-1;
    int m=b.size()-1;
    string tmp = a;
    vector <string> ans;
    ans.push_back(tmp);
    while(n>0 && m>0)
    {
        if( dp[n-1][m-1]+((a[n]!=b[m]))==dp[n][m]) {
            tmp[n] = b[m];
            if(a[n]!=b[m])
            {
                ans.push_back(string("Replace: ") + a[n] + string(" with ") + b[m]);
            }
            else {
                n--,m--;
                continue;
            }
            n--;m--;
        }
        else if(dp[n-1][m]+1==dp[n][m]) {
            tmp.erase(n,1);
        ans.push_back(string("Remove: ") + a[n]);
            n--;
        }
        else if(dp[n][m-1]+1==dp[n][m]) {
            string t;
            t.push_back(b[m]);
            tmp.insert(n , t);
            ans.push_back(string("Insert: ") + b[m]);
            m--;
        }
        else if(n>1 && m>1 && a[n]==b[m-1] && a[n-1]==b[m]) { 
            ans.push_back(string("Rotate ") + a[n] + string(" and ") + a[n-1]);
            n-=2;
            m-=2;
        }
        ans.push_back(tmp);
    }
    while(m>0) {
        string t;
        t.push_back(b[m]);
        tmp.insert(n+1 , t);
        ans.push_back(string("Insert: ") + b[m]);
        ans.push_back(tmp);
        m--;
    }
    while(n>0) {
        tmp.erase(n,1);
        ans.push_back(string("Remove: ") + a[n]);
        ans.push_back(tmp);
        n--;
    }
//    reverse(ans.begin(), ans.end());

    for(auto it: ans)
        cout << it << endl;
}