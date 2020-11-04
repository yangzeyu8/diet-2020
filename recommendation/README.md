# Ideas about Recipe Recommendation

## Introduction

| Field           | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Recipe name     | 2-Step Chicken                                               |
| Serving         | 4                                                            |
| Group name      | not known                                                    |
| Calories        | 45.25                                                        |
| Protein         | 4.25                                                         |
| Carbohydrate    | 1.25                                                         |
| Fat             | 2.5                                                          |
| Ingredients     | ['1 tablespoon  vegetable oil', '2 Boneless chicken breasts', '1 can cream of chicken soup  (10 ounces)', '1/2 cup water'] |
| Recipe source   | https://www.choosemyplate.gov/recipes/supplemental-nutrition-assistance-program-snap/2-step-chicken |
| Breakfast judge | not breakfast                                                |

## Recommendation Model

### A. Nutrition Goal

#### Variables:

1. Chose recipes

   This vectors can return multiple recipes. The elements in this vector must be 0, 0.5 or 1.

$$
R = 
\begin{bmatrix}
 R_1
 \\R_2
 \\R_3
 \\...
 \\R_R
\end{bmatrix}
$$

#### Parameters:

1. Nutrition information of recipes (web scraping)
2. Upper and lower nutrition boundaries (provided by user)

3. The most comfortable nutrition goal (provided by user)

4. The discomfort parameter (set by the programmer or learnt from learning algorithms)

$$
N = 
\begin{bmatrix}
 N^{calorie}
 \\N^{protein}
 \\N^{carbohydrate}
 \\N^{fat}
\end{bmatrix}
$$

#### Constraints:

1. Calories
   $$
   \begin{array}{c}
     N_{min}^{calorie}\lt  {\textstyle \sum_{i}^{}} N_{i}^{calorie} \lt N_{max}^{calorie}
   \end{array},\forall i\in R
   $$
   

2. Protein
   $$
   \begin{array}{c}
     N_{min}^{protein}\lt  {\textstyle \sum_{i}^{}} N_{i}^{protein} \lt N_{max}^{protein}
   \end{array},\forall i\in R
   $$
   

3. Carbohydrate
   $$
   \begin{array}{c}
     N_{min}^{carbohydrate}\lt  {\textstyle \sum_{i}^{}} N_{i}^{carbohydrate} \lt N_{max}^{carbohydrate}
   \end{array},\forall i\in R
   $$
   

4. Fat
   $$
   \begin{array}{c}
     N_{min}^{fat}\lt  {\textstyle \sum_{i}^{}} N_{i}^{fat} \lt N_{max}^{fat}
   \end{array},\forall i\in R
   $$

#### Objective Function:

Model the discomfort as a cost function
$$
C_{}^{N}=\beta_{}^{N}{\textstyle \sum_{n}^{}}|{\textstyle \sum_{i}^{}} R_iN_{i}^{n}-N_{ref}^{n}|,\forall i\in R,\forall n\in N
$$

#### Exceptions:

For following situations, just remove corresponding recipes from the domain.

1. Allergic
2. Special eating habits

### B. Rating

#### Parameters:

1. For a family

   This vector represents family members.
   $$
   U= 
   \begin{bmatrix}
    U_1
    \\U_2
    \\...
    \\U_U
   \end{bmatrix}
   $$
   

2. How single user like recipes

   The elements in this vector must be integers from 0 to 5. It represents the rating for each recipe.
   $$
   F^{u} = 
   \begin{bmatrix}
    F_1
    \\F_2
    \\F_3
    \\...
    \\F_R
   \end{bmatrix},\forall u \in U
   
   \\ F = 
   \begin{bmatrix}
   F^1,F^2,...,F^U
   
   \end{bmatrix}
   $$

#### Objective Function:

Model the discomfort as a cost function
$$
C_{}^{F}=\beta^F{\textstyle \sum_{u}^{}}{\textstyle \sum_{i}^{}}R_i|F_{i}^{u}-5|^2,\forall i\in R,\forall u\in U
\\ C = C^N+C^F
$$

## Updating Rating Parameters

### Similarity

$$
N_i =\begin{bmatrix}
 N_i^{calorie}
 \\N_i^{protein}
 \\N_i^{carbohydrate}
 \\N_i^{fat}
\end{bmatrix},N_j =\begin{bmatrix}
 N_j^{calorie}
 \\N_j^{protein}
 \\N_j^{carbohydrate}
 \\N_j^{fat}
\end{bmatrix}, \forall i,j \in R
$$

#### 1. One try: Mahalanobis distance clustering

$$
d(N_i,N_j)=\sqrt{(N_i-N_j)^T {\textstyle \sum_{}^{-1}}(N_i-N_j) }
$$

#### 2. Another try: CNN

### Updating

1. Collect ratings of a number of recipes of a user.

2. Use it as traing set to classify remaining recipes.

## Sorting

### Popularity

$$
Popularity = {v\over v+m}R+{v\over v+m}C
$$

R - Average score for a recipe vote
v - Number of valid voters
m - Minimum number of voters
C - Average of all recipe
