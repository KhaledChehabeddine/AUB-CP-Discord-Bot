#include <iostream>
#include <vector>
#include <queue>
#include <string>

template <typename T>
class Node {

private:
  T x;
  Node<T>* parent = nullptr;
  Node<T>* left = nullptr;
  Node<T>* right = nullptr;

public:
  Node<T> (T _x, Node<T>* p, Node<T>* l, Node<T>* r){
    x = _x; parent = p; left = l; right = r;
  }
  Node<T> (T _x, Node<T>* p){
    (*this) = Node<T>(_x, p, nullptr, nullptr);
  }
  Node<T> (T _x, T _p, T _l, T _r){
    (*this) = Node<T>(_x, new Node<T>(_p), new Node<T>(_l), new Node<T>(_r));
  }
  Node<T> (T _x) {x = _x;}

  T getX() {return x;}
  Node<T>* getParent() {return parent;}
  Node<T>* getLeft() {return left;}
  Node<T>* getRight() {return right;}

  void setX(T _x) {x = _x;}
  void setParent(Node<T>* p) {parent = p;}
  void setLeft(Node<T>* l) {left = l;}
  void setRight(Node<T>* r) {right = r;}
  void setParent(T _p) {parent = new Node<T>(_p);}
  void setLeft(T _l) {left = new Node<T>(_l);}
  void setRight(T _r) {right = new Node<T>(_r);}

  int nb_of_children(){
    return (left != nullptr) + (right != nullptr);
  }

  bool isLeaf(){
    return nb_of_children() == 0;
  }

  void print(){
    std::cout << "NODE: \n";
    std::cout << "|  x      = " << x << '\n';
    std::cout << "|  parent = " << (parent == nullptr ? -1 : parent->getX()) << '\n';
    std::cout << "|  left   = " << (left == nullptr ? -1 : left->getX()) << '\n';
    std::cout << "|  right  = " << (right == nullptr ? -1 : right->getX()) << '\n';
    std::cout << "------------\n";
  }
};

template <typename T>
class BST {

private:
  Node<T>* root = nullptr;
  int sz = 0;

  void add(Node<T>* u, Node<T>* p, T x, bool left){
    if (!u) {
      u = new Node<T>(x, p);
      if (left) p->setLeft(u); else p->setRight(u);
      return;
    }
    if (x < u->getX()) add(u->getLeft(), u, x, 1);
    else add(u->getRight(), u, x, 0);
  }

  int height(Node<T>* u){
    if (!u) return 0;
    return 1 + std::max(height(u->getLeft()), height(u->getRight()));
  }

  Node<T>* find(Node<T>* u, T x){
    if (!u) return u;
    if (x < u->getX()) return find(u->getLeft(), x);
    if (x > u->getX()) return find(u->getRight(), x);
    return u;
  }

  void dfs(Node<T>* u, std::vector<Node<T>*>& v){
    if (!u) return;
    v.push_back(u);
    dfs(u->getLeft()); dfs(u->getRight());
  }

  void print_indented(Node<T>* u, std::string x, int l){
    if (!u) return;
    std::cout << x << (l == 1 ? "lt_" : (l == 0 ? "rt_" : "")) << u->getX() << '\n';
    print_indented(u->getLeft(), x + "| ", 1);
    print_indented(u->getRight(), x + "| ", 0);
  }

public:
  BST() {}

  int size() {return sz;}
  bool isEmpty() {return size() == 0;}
  int height() {return height(getRoot()) - 1;}
  Node<T>* getRoot() {return root;}

  Node<T>* getMin(Node<T>* u){
    while (u && u->getLeft()) u = u->getLeft();
    return u;
  }

  void add(T x){
    if (!root) root = new Node<T>(x);
    else add(getRoot(), nullptr, x, 0);
  }

  Node<T>* find(T x) {return find(getRoot(), x);}

  void remove(T x){
    Node<T>* u = find(x);
    if (!u) return;
    --sz;
    if (u->isLeaf()){
      Node<T>* p = u->getParent();
      if (!p) root = nullptr;
      else {
        if (p->getLeft() == u) p->setLeft(nullptr);
        else p->setRight(nullptr);
      }
      return;
    }
    if (!u->getRight()){
      Node<T>* p = u->getParent();
      if (!p) root = nullptr;
      else {
        if (p->getLeft() == u) p->setLeft(u->getLeft());
        else p->setRight(u->getLeft());
      }
      return;
    }
    if (!u->getLeft()){
      Node<T>* p = u->getParent();
      if (!p) root = nullptr;
      else {
        if (p->getLeft() == u) p->setLeft(u->getRight());
        else p->setRight(u->getRight());
      }
      return;
    }
    ++sz;
    Node<T>* successor = getMin(u->getRight());
    const T k = successor->getX();
    remove(k); u->setX(k);
    return;
  }

  void print(Node<T>* u){
    if (!u) return;
    std::cout << u->getX() << ' ';
    print(u->getLeft()); print(u->getRight());
  }

  std::vector<Node<T>*> dfs(Node<T>* u) {
    std::vector<Node<T>*> v;
    dfs(u, v);
    return v;
  }

  std::vector<Node<T>*> bfs(Node<T>* u){
    std::vector<Node<T>*> arr;
    std::queue<Node<T>*> q;
    if (u) q.push(u);
    while (!q.empty()){
      Node<T>* v = q.front(); q.pop();
      arr.push_back(v);
      if (v->getLeft()) q.push(v->getLeft());
      if (v->getRight()) q.push(v->getRight());
    }
    return arr;
  }

  void print_indented(){
    print_indented(getRoot(), "", -1);
  }
};

int main(){
  BST<int> tree;
  for (int i = 1; i <= 3; ++i){
    tree.add(2 * i); tree.add(i); tree.add(2 * i + 1);
  }
  tree.print_indented();
}