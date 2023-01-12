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
                double rotate_lim = 0., double scale_factor = 1.,
                bool isSubstract = false, bool isRotate = false,
                bool isScale = false)
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
                for (int k = 0; k < dim; k++)
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
            if (isScale)
            {
                for (int k = 0; k < dim; k++)
                    tempx[k] = tempx[k] * scale_factor;
            }
            double res = (*problem)(tempx);
            y.push_back(res);
        }
        y_sets.push_back(y);
    }
    ofstream fout;
    stringstream ss;
    ss << "../results/data/scale/" << to_string(problem_id) << "_"
       << to_string(experiment_id) << "_" << to_string(subtract_lim) << "_"
       << to_string(rotate_lim) << "_" << to_string(scale_factor) << "_"
       << to_string(isSubstract) << "_" << to_string(isRotate) << "_"
       << to_string(isScale) << ".txt";
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

void compute_rotation(const long rotation_seed, const int n_variables)
{
    const auto random_vector = ioh::common::random::bbob2009::normal(
        static_cast<size_t>(n_variables) * n_variables, rotation_seed);
    auto matrix = std::vector<std::vector<double>>(
        n_variables, std::vector<double>(n_variables));

    // reshape
    for (auto i = 0; i < n_variables; i++)
        for (auto j = 0; j < n_variables; j++)
            matrix[i][j] =
                random_vector.at(static_cast<size_t>(j) * n_variables + i);


    /*1st coordinate is row, 2nd is column.*/
    for (long i = 0; i < n_variables; i++)
    {
        for (long j = 0; j < i; j++)
        {
            auto prod = 0.0;
            for (auto k = 0; k < n_variables; k++)
                prod += matrix[k][i] * matrix[k][j];

            for (auto k = 0; k < n_variables; k++)
                matrix[k][i] -= prod * matrix[k][j];
        }
        auto prod = 0.0;
        for (auto k = 0; k < n_variables; k++)
            prod += matrix[k][i] * matrix[k][i];

        for (auto k = 0; k < n_variables; k++)
            matrix[k][i] /= sqrt(prod);
    }
    for (int i = 0; i < matrix[0].size(); i++)
        cout << matrix[0][i] << " ";
    cout << endl;
    // return matrix;
}

int main()
{
    CecUtils cec_utils;
    vector<vector<vector<double>>> x_sets;
    read_x(x_sets);


    // compute_rotation(114514, 10);
    // vector<double> factors;
    // int factor_size = 20;
    // for (int i = 0; i < factor_size; i++)
    //     factors.push_back((i + 1) * 100. / factor_size);

    vector<double> factors = {0.015625, 0.03125, 0.0625, 0.125, 0.25,
                              0.5,      1.,      2.,     4.,    8.,
                              16.,      32.,     64.,    128.};


    for (int problem_id = 1; problem_id <= 5; problem_id++)
    {
        experiment(x_sets, problem_id);
        for (int factor_ind = 0; factor_ind < factors.size(); factor_ind++)
        {
            // for (int experiment_id = 0; experiment_id < 10; experiment_id++)
            // {
            experiment(x_sets, problem_id, 0, 0.0, 0.0, factors[factor_ind],
                       false, false, true);
            // }
        }
    }
}