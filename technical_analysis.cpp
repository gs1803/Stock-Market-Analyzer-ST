#include <pybind11/pybind11.h>
#include <pybind11/stl.h>  
#include "technical_analysis.h"
namespace py = pybind11;

vector<double> TechnicalAnalysis::rsi_calculation(const vector<double>& data, int lookback) {
    vector<double> returns(data.size(), 0.0);
    vector<double> up(data.size(), 0.0);
    vector<double> down(data.size(), 0.0);
    
    for (size_t i = 1; i < data.size(); ++i) {
        returns[i] = data[i] - data[i - 1];
        if (returns[i] < 0) {
            down[i] = -returns[i];
        } else {
            up[i] = returns[i];
        }
    }

    vector<double> up_ewm = exponential_moving_average(up, lookback);
    vector<double> down_ewm = exponential_moving_average(down, lookback);

    vector<double> rs(up_ewm.size());
    transform(up_ewm.begin(), up_ewm.end(), down_ewm.begin(), rs.begin(), [](double u, double d) { return u / d; });

    vector<double> rsi(rs.size());
    transform(rs.begin(), rs.end(), rsi.begin(), [](double r) { return 100 - (100 / (1 + r)); });

    return vector<double>(rsi.begin(), rsi.end());
}

vector<vector<double>> TechnicalAnalysis::macd_calculations(const vector<double>& data, int slow, int fast, int smooth) {
    vector<double> exp1 = exponential_moving_average(data, fast);
    vector<double> exp2 = exponential_moving_average(data, slow);
    vector<double> macd(data.size());
    transform(exp1.begin(), exp1.end(), exp2.begin(), macd.begin(), minus<double>());

    vector<double> signal = exponential_moving_average(macd, smooth);
    vector<double> hist(macd.size());
    transform(macd.begin(), macd.end(), signal.begin(), hist.begin(), minus<double>());

    return {macd, signal, hist};
}

vector<double> TechnicalAnalysis::sma_calculations(const vector<double>& data, int window) {
    vector<double> sma(data.size(), 0.0);
    double sum = accumulate(data.begin(), data.begin() + window, 0.0);
    for (size_t i = window; i < data.size(); ++i) {
        sma[i] = sum / window;
        sum += data[i] - data[i - window];
    }
    return sma;
}

pair<vector<double>, vector<double>> TechnicalAnalysis::bollinger_bands_calculations(const vector<double>& data, const vector<double>& sma, int window) {
    vector<double> std(data.size(), 0.0);
    for (size_t i = window; i < data.size(); ++i) {
        double sum = 0.0;
        for (size_t j = i - window + 1; j <= i; ++j) {
            sum += pow(data[j] - sma[i], 2);
        }
        std[i] = sqrt(sum / window);
    }
    
    vector<double> upper_band(sma.size()), lower_band(sma.size());
    transform(sma.begin(), sma.end(), std.begin(), upper_band.begin(), [](double m, double s) { return m + 2 * s; });
    transform(sma.begin(), sma.end(), std.begin(), lower_band.begin(), [](double m, double s) { return m - 2 * s; });

    return {upper_band, lower_band};
}

pair<vector<double>, vector<double>> TechnicalAnalysis::donchian_breakout_calculations(const vector<double>& data, const vector<double>& high_prices, const vector<double>& low_prices, int window) {
    vector<double> upper_channel(data.size(), 0.0);
    vector<double> lower_channel(data.size(), 0.0);
    
    for (size_t i = window - 1; i < data.size(); ++i) {
        upper_channel[i] = *max_element(high_prices.begin() + i - window + 1, high_prices.begin() + i + 1);
        lower_channel[i] = *min_element(low_prices.begin() + i - window + 1, low_prices.begin() + i + 1);
    }

    return {upper_channel, lower_channel};
}

pair<vector<double>, vector<double>> TechnicalAnalysis::implement_rsi(const vector<double>& data, const vector<double>& rsi) {
    vector<double> rsi_buy_price(data.size(), nan(""));
    vector<double> rsi_sell_price(data.size(), nan(""));
    vector<int> rsi_signal(data.size(), 0);
    int signal = 0;

    for (size_t i = 1; i < rsi.size(); ++i) {
        if (rsi[i - 1] > 30 && rsi[i] < 30 && signal != 1) {
            rsi_buy_price[i] = data[i];
            signal = 1;
            rsi_signal[i] = signal;
        } else if (rsi[i - 1] < 70 && rsi[i] > 70 && signal != -1) {
            rsi_sell_price[i] = data[i];
            signal = -1;
            rsi_signal[i] = signal;
        }
    }

    return {rsi_buy_price, rsi_sell_price};
}

pair<vector<double>, vector<double>> TechnicalAnalysis::implement_macd(const vector<double>& data, const vector<vector<double>>& data_macd) {
    vector<double> macd_buy_price(data.size(), nan(""));
    vector<double> macd_sell_price(data.size(), nan(""));
    vector<int> macd_signal(data.size(), 0);
    int signal = 0;

    for (size_t i = 0; i < data_macd[0].size(); ++i) {
        if (data_macd[0][i] > data_macd[1][i] && signal != 1) {
            macd_buy_price[i] = data[i];
            signal = 1;
            macd_signal[i] = signal;
        } else if (data_macd[0][i] < data_macd[1][i] && signal != -1) {
            macd_sell_price[i] = data[i];
            signal = -1;
            macd_signal[i] = signal;
        }
    }

    return {macd_buy_price, macd_sell_price};
}

pair<vector<double>, vector<double>> TechnicalAnalysis::implement_bollinger(const vector<double>& data, const vector<double>& lower_bb, const vector<double>& upper_bb) {
    vector<double> bollinger_buy_price(data.size(), nan(""));
    vector<double> bollinger_sell_price(data.size(), nan(""));
    vector<int> bollinger_signal(data.size(), 0);
    int signal = 0;

    for (size_t i = 1; i < data.size(); ++i) {
        if (data[i - 1] > lower_bb[i - 1] && data[i] < lower_bb[i] && signal != 1) {
            bollinger_buy_price[i] = data[i];
            signal = 1;
            bollinger_signal[i] = signal;
        } else if (data[i - 1] < upper_bb[i - 1] && data[i] > upper_bb[i] && signal != -1) {
            bollinger_sell_price[i] = data[i];
            signal = -1;
            bollinger_signal[i] = signal;
        }
    }

    return {bollinger_buy_price, bollinger_sell_price};
}

pair<vector<double>, vector<double>> TechnicalAnalysis::implement_donchian(const vector<double>& data, const vector<double>& upper_channel, const vector<double>& lower_channel) {
    vector<double> donchian_buy_price(data.size(), nan(""));
    vector<double> donchian_sell_price(data.size(), nan(""));
    vector<int> donchian_signal(data.size(), 0);
    int signal = 0;

    for (size_t i = 1; i < data.size(); ++i) {
        if (data[i] > upper_channel[i - 1] && data[i - 1] <= upper_channel[i - 1] && signal != 1) {
            donchian_buy_price[i] = data[i];
            signal = 1;
            donchian_signal[i] = signal;
        } else if (data[i] < lower_channel[i - 1] && data[i - 1] >= lower_channel[i - 1] && signal != -1) {
            donchian_sell_price[i] = data[i];
            signal = -1;
            donchian_signal[i] = signal;
        }
    }

    return {donchian_buy_price, donchian_sell_price};
}

vector<double> TechnicalAnalysis::exponential_moving_average(const vector<double>& data, int period) {
    vector<double> ewm(data.size(), 0.0);
    double alpha = 2.0 / (period + 1);
    ewm[0] = data[0];
    for (size_t i = 1; i < data.size(); ++i) {
        ewm[i] = alpha * data[i] + (1 - alpha) * ewm[i - 1];
    }
    return ewm;
}

PYBIND11_MODULE(technical_analysis_module, m) {
    py::class_<TechnicalAnalysis>(m, "TechnicalAnalysis")
        .def(py::init<>())
        .def("rsi_calculation", &TechnicalAnalysis::rsi_calculation)
        .def("macd_calculations", &TechnicalAnalysis::macd_calculations)
        .def("sma_calculations", &TechnicalAnalysis::sma_calculations)
        .def("bollinger_bands_calculations", &TechnicalAnalysis::bollinger_bands_calculations)
        .def("donchian_breakout_calculations", &TechnicalAnalysis::donchian_breakout_calculations)
        .def("implement_rsi", &TechnicalAnalysis::implement_rsi)
        .def("implement_macd", &TechnicalAnalysis::implement_macd)
        .def("implement_bollinger", &TechnicalAnalysis::implement_bollinger)
        .def("implement_donchian", &TechnicalAnalysis::implement_donchian);
}
