# SatisSolver 

> /!\ This ideas presented here will certainly evolve as I progress through the game with my friends. The first idea is to devlop a recipe optimizer module to optimize the production process by minimizing costs and maximizing efficiency.
  
Consider the following example. A quantity of 4 screws is made of 1 iron rod. It can be  
manufactured at constructor with a cycle time of 6, i.e., 4 screws are made every 6 seconds.  
At different stages of the game we need to produce some quantities of resources to unlock subsequent stages. 
To reduce waiting time, we need to parallelize production. The question is how to optimally achieve the desired resources?   
In the game there are multiple resources and multiple ways to produce them, the  
computation by hand can quickly become complicated. Hence, this simple project aims to solve this problem using some mathematical optimization.  

**Vocabulary:**  
- A recipe is a way to produce a resource from other resources.  
- A machine is an abstraction of a recipe executor, it takes a set of input and gives a set of output within a duration given in seconds, known as the cycle time. 
- A production rate is the quantity of output produced by a machine every second. It is the inverse of the cycle time.  
  
**Remarks:** 
1. In the game a machine can be a constructor, a smelter, a foundry, etc. But they are all different representations of the same concept: a recipe executor. 
2. Every machine is configured to execute only one kind of recipe. 
  
  
## Mathematical model  
  
We denote by $R$ the set of recipes and by $K$ the set of resources.  
  
### Matrix representation of recipes  
For every recipe $r \in R$, we define a vector $q_r \in \mathbb{R}^{|K|}$ such that $q_{kr}$ is the quantity of resource $k$ involved in recipe $r$.  
  
The quantity $q_kr \in \mathbb{R}^{|K|}$ is:  
  
- negative when the resource $k$ is consumed by the recipe $r$
- positive when resource $k$ is produced by the recipe $r$
- zero when the resource $k$ is not involved at all in the recipe.  
  
We can represent this as a matrix  where every column represents a recipe and ever line represents a resource.  
$$  
\mathbf{Q} =  
\begin{bmatrix}  
q_{11} & q_{21} & \dots & q_{R1} \\  
q_{12} & q_{22} & \dots & q_{R2} \\  
\vdots & \vdots & \ddots & \vdots \\  
q_{1K} & q_{2K} & \dots & q_{RK} \\  
\end{bmatrix}  
$$  
  
**Instantaneous production hypothesis:**  
To take into account the time needed to produce every item of every recipe, we need to divide by the cycle time the output quantities of every recipe.  
Fo example, `6 iron plate + 12 screw  --(12 seconds)--> 1 reinforced iron plate` becomes, `6 iron plate + 12 screw  ----> 1/12 reinforced iron plate`, as if the production was instantaneous.   In other words, for the outputs of the recipe we use the production rates instead of the quantities, 
  
**Example:** So if we only had two recipes and 4 ingredients (iron rod, iron plate, screw, reinforced iron plate) in the game: `6 iron plate + 12 screw --(12 seconds)--> 1 reinforced iron plate` and `1 iron rod --(6 seconds)--> 4 screw`, the matrix would be:   
  
$$  
\begin{bmatrix}  
-6 & 0 \\  
0 & -1 \\  
-12 & \frac{4}{6} \\  
\frac{1}{12} & 0 \\  
\end{bmatrix}  
$$  
  
which can be read as:  
  
| Empty Column           | Recipe 1 | Recipe 2 |  
|------------------------|----------|----------|  
| iron plate             | -6        | 0        |  
| iron rod               | 0        | -1        |  
| screw                  | -12       | 4/6     |  
| reinforced iron plate  | 1/12    | 0        |  
  
  The data of such a matrix is supposed to be known at advance. 
  
  **Property:** For each line representing a resource $k$, the sum of quantities corresponds to the actual production rate if every recipe was executed by only one machine. 
    
### Decision variables
For every recipe $r \in k$ we need to determine how many time is executed in parallel, which is equivalent to how many machines are executing such a resource — since each machine is assigned to exactly one recipe.  We denote such variable by $x_r geq 0$. The values of those variables will be determined by the algorithm that solves the model. 

**Remark:** Another, less straightforward decision variable will be introduced in the constraints section because it's less ambiguous to explain it there.

### Constraints
The idea is that the user precise the desired production rate, for example, 20 reinforced iron plate and 40 wires per second. The algorithm will then works backward and figure out how to achieve such rates, or at least how to be as closer as possible to those rates.  
 For every resource $k \in K$ we need to precise the desired production rate, denoted by $d_k$.

**How to know what is the actual production rate for resource $k \in K$?**: 
Since: 
- The quantity produced by every recipe $r$ is $q_{kr}$
- There is $x_r$ machines executing the recipe $r$
-  Multiple recipes can involve a resource $k$ (for inputsor outputs)
Then the actual production rate is $\sum_{r \in R} q_{kr} x_r$ which is simply a scary notation for $q_{kr_1} \times x_{r_1} + q_{kr_2}x_{r_2} + \dots + q_{kr_R}x_{r_R}$ 

**Production rate constraint:**
To translate the fact that we need to match a desired production rate for a resource $k$, we introduce the following inequality: $q_{kr_1} \times x_{r_1} + q_{kr_2}x_{r_2} + \dots + q_{kr_R}x_{r_R} \geq d_k$ which means, the actual production rate is at least equal to the desired production rate given by the user. 
However, if we want the algorithm to always respect such inequalities for all resources, we may not find a feasible solution. To make this more intresting from a user point of view, we introduce another decision variable $y_k \geq 0$ such that:  $q_{kr_1} \times x_{r_1} + q_{kr_2}x_{r_2} + \dots + q_{kr_R}x_{r_R} + y_k \geq d_k$. Its values will be determined by the algorithn. It represents the "lacking quantity" to acheive the desired output $d_k$.  We will see later that we aim to minimize the sum of all the $y_k$. Thus we allow to produce less than the desired production rate but we try to prevent this as much as possible. This can be understood as minimizing the waste. Note that in an optimal solution, we will be able to produce exactly at the desired production rate $d_k$, this decision variables $y_k$ will be set to $0$ by the algorithm. 

### Objective function
- For each recipe $r \in R$ there is production cost denoted by $c_r$; it represents power usage needed to execute the recipe $r$. The aim is to reduce the total cost, that $\sum_{r \in R} c_r x_r$ which is, again, a scary notation for $c_{r_1} \times x_{r_1} + c_{r_2}x_{r_2} + \dots + c_{r_R}x_{r_R}$. 
- Remember also that we needed to reduce the total "lacking quantities" $y_r$, which is $\sum_{r \in R} y_r$.  

The objective function is the sum of both of those terms. 
### Final model 
To sum up:
The decision variables: $x_r \geq  0, y_r \geq 0$
The objective function:  $\sum_{r \in R} c_r x_r + \sum_{r \in R} y_r$
The constraint: $q_{kr_1} \times x_{r_1} + q_{kr_2}x_{r_2} + \dots + q_{kr_R}x_{r_R} + y_k \geq d_k$