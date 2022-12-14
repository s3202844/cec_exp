#include "ioh.hpp"

using namespace std;
using namespace ioh::problem::cec;
using namespace ioh::problem::transformation::objective;
using namespace ioh::problem::transformation::variables;

const int num_sampling = 1000;
const int num_x = 100;
const int dim = 2;

void read_x(vector<vector<vector<double>>> &x_sets)
{
    ifstream fin;
    fin.open("results/samplingX.txt", ios::in);
    double x0, x1;
    string header;
    for (int i = 0; i < num_sampling; i++)
    {
        fin >> header;
        fin >> header;
        vector<vector<double>> x;
        for (int j = 0; j < num_x; j++)
        {
            fin >> header >> x0 >> x1;
            x.push_back({x0, x1});
        }
        x_sets.push_back(x);
    }
    fin.close();
}

void write_y(vector<vector<double>> y_sets, string marker)
{
    ofstream fout;
    stringstream ss;
    ss << "results/" << marker << ".txt";
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
    const auto &problem_factory =
        ioh::problem::ProblemRegistry<ioh::problem::CEC2022>::instance();

    read_x(x_sets);
    for (int problem_id = 1; problem_id <= 5; problem_id++)
    {
        vector<vector<double>> y_sets, y_sets_trans;
        auto problem = problem_factory.create(problem_id, 1, dim);

        int angle = rand() % 180;
        double theta = angle / 180. * M_PI;
        vector<double> m = {cos(theta), -sin(theta), sin(theta), cos(theta)};

        vector<double> os;
        for (size_t i = 0; i < problem->optimum().x.size(); i++)
        {
            double ox = rand() / double(RAND_MAX) * 200. - 100. -
                problem->optimum().x[i];
            os.push_back(-ox);
        }


        for (int i = 0; i < num_sampling; i++)
        {
            vector<double> y, y_trans;
            for (size_t j = 0; j < num_x; j++)
            {
                vector<double> tempx = {x_sets[i][j][0], x_sets[i][j][1]};
                cec_utils.sr_func(tempx, os, m, 1.0, true, true, dim);
                double tmp1 = (*problem)(x_sets[i][j]);
                double tmp2 = (*problem)(tempx);
                y.push_back(tmp1);
                y_trans.push_back(tmp2);
            }
            y_sets.push_back(y);
            y_sets_trans.push_back(y_trans);
        }
        write_y(y_sets, "origin_" + to_string(problem_id));
        write_y(y_sets_trans, "affine_" + to_string(problem_id));
    }
}