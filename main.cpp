#include "ioh.hpp"

using namespace std;
using namespace ioh::problem::cec;
using namespace ioh::problem::transformation::objective;
using namespace ioh::problem::transformation::variables;

const int num_sampling = 100;
const int num_x = 1000;
const int dim = 10;

void read_x(vector<vector<vector<double>>> &x_sets)
{
    ifstream fin;
    fin.open("../results/samplingX.txt", ios::in);
    double read_cache;
    string header;
    for (int i = 0; i < num_sampling; i++)
    {
        for (int j = 0; j < dim; j++)
            fin >> header;
        vector<vector<double>> x;
        for (int j = 0; j < num_x; j++)
        {
            fin >> header;
            vector<double> x_cache;
            for (int k = 0; k < dim; k++)
            {
                fin >> read_cache;
                x_cache.push_back(read_cache);
            }
            x.push_back(x_cache);
        }
        x_sets.push_back(x);
    }
    fin.close();
}

void experiment(vector<vector<vector<double>>> &x_sets, int problem_id,
                int experiment_id = 0, double subtract_lim = 0.,
                double rotate_lim = 0., bool isSubstract = false,
                bool isRotate = false)
{
    const auto &problem_factory =
        ioh::problem::ProblemRegistry<ioh::problem::CEC2022>::instance();
    auto problem = problem_factory.create(problem_id, 1, dim);
    vector<vector<double>> y_sets;
    for (int i = 0; i < num_sampling; i++)
    {
        vector<double> y;
        for (size_t j = 0; j < num_x; j++)
        {
            vector<double> tempx(x_sets[i][j]);
            if (isSubstract)
            {
                vector<double> offset;
                for (int i = 0; i < dim; i++)
                    offset.push_back((rand() / double(RAND_MAX) * 200. - 100.) *
                                     subtract_lim / 100.);
                subtract(tempx, offset);
            }
            // if (isRotate)
            // {
            //     int angle = rand() % 180;
            //     double theta = angle / 180. * M_PI;
            //     vector<double> m = {cos(theta), -sin(theta), sin(theta),
            //                         cos(theta)};
            // }
            double res = (*problem)(tempx);
            y.push_back(res);
        }
        y_sets.push_back(y);
    }
    ofstream fout;
    stringstream ss;
    ss << "../results/data/" << to_string(problem_id) << "_"
       << to_string(experiment_id) << "_" << to_string(subtract_lim) << "_"
       << to_string(rotate_lim) << "_" << to_string(isSubstract) << "_"
       << to_string(isRotate) << ".txt";
    fout.open(ss.str(), ios::out);
    for (size_t i = 0; i < y_sets.size(); i++)
    {
        for (size_t j = 0; j < y_sets[i].size(); j++)
        {
            fout << y_sets[i][j] << " ";
        }
        fout << endl;
    }
    fout.close();
}


int main()
{
    CecUtils cec_utils;
    vector<vector<vector<double>>> x_sets;
    read_x(x_sets);

    vector<double> factors;
    int factor_size = 20;
    for (int i = 0; i < factor_size; i++)
        factors.push_back((i + 1) * 100. / factor_size);

    for (int problem_id = 1; problem_id <= 5; problem_id++)
    {
        experiment(x_sets, problem_id);
        for (int factor_ind = 0; factor_ind < factors.size(); factor_ind++)
        {
            for (int experiment_id = 0; experiment_id < 10; experiment_id++)
            {
                experiment(x_sets, problem_id, experiment_id,
                           factors[factor_ind], 0.0, true, false);
            }
        }
    }
}