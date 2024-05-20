#ifndef TECHNICALANALYSIS_H
#define TECHNICALANALYSIS_H

#include <vector>
#include <utility>
#include <cmath>
#include <numeric>
#include <algorithm>
#include <limits>

using namespace std;

class TechnicalAnalysis {
    public:
        vector<double> rsi_calculation(const vector<double>& data, int lookback);
        vector<vector<double>> macd_calculations(const vector<double>& data, int slow, int fast, int smooth);
        vector<double> sma_calculations(const vector<double>& data, int window);
        pair<vector<double>, vector<double>> bollinger_bands_calculations(const vector<double>& data, const vector<double>& sma, int window);
        pair<vector<double>, vector<double>> donchian_breakout_calculations(const vector<double>& data, const vector<double>& high_prices, const vector<double>& low_prices, int window);
        pair<vector<double>, vector<double>> implement_rsi(const vector<double>& data, const vector<double>& rsi);
        pair<vector<double>, vector<double>> implement_macd(const vector<double>& data, const vector<vector<double>>& data_macd);
        pair<vector<double>, vector<double>> implement_bollinger(const vector<double>& data, const vector<double>& lower_bb, const vector<double>& upper_bb);
        pair<vector<double>, vector<double>> implement_donchian(const vector<double>& data, const vector<double>& upper_channel, const vector<double>& lower_channel);

    private:
        vector<double> exponential_moving_average(const vector<double>& data, int period);
};

#endif
