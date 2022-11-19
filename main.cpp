#include "ioh.hpp"

using namespace std;
using namespace ioh::problem::cec;
using namespace ioh::problem::transformation::objective;

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
    vector<vector<vector<double>>> x_sets;
    const auto &problem_factory =
        ioh::problem::ProblemRegistry<ioh::problem::CEC2022>::instance();

    read_x(x_sets);
    for (int problem_id = 1; problem_id <= 5; problem_id++)
    {
        vector<vector<double>> y_sets, y_sets_scale;
        auto problem = problem_factory.create(problem_id, 1, dim);

        for (int i = 0; i < num_sampling; i++)
        {
            vector<double> y, y_scale;
            for (size_t j = 0; j < num_x; j++)
            {
                double tmp = (*problem)(x_sets[i][j]);
                y.push_back(tmp);
                y_scale.push_back(scale(tmp, 2.0));
            }
            y_sets.push_back(y);
            y_sets_scale.push_back(y_scale);
        }
        write_y(y_sets, "origin_" + to_string(problem_id));
        write_y(y_sets_scale, "scale_2_" + to_string(problem_id));
    }
}