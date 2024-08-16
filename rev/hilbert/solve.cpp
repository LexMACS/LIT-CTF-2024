#include <stdexcept>
#include <string>
#include <variant>
#include <stdexcept>
#include <memory>
#include <iostream>

// proposition
struct Prop;
using Pro = std::shared_ptr<Prop const>;

struct Prop {
    struct Primitive {
        std::string const s;

        bool operator==(Primitive const& other) const {
            return s == other.s;
        }

        std::string as_math() const {
            return s;
        }

        std::string as_sol() const {
            return s;
        }
    };

    // 若 = `→`
    struct Implication {
        Pro const p;
        Pro const q;

        bool operator==(Implication const& other) const {
            return *p == *other.p && *q == *other.q;
        }

        std::string as_math() const {
            return "(" + p->as_math() + " → " + q->as_math() + ")";
        }

        std::string as_sol() const {
            return "若<" + p->as_sol() + "," + q->as_sol() + ">";
        }
    };

    // 非 = `¬`
    struct Negation {
        Pro const p;

        bool operator==(Negation const& other) const {
            return *p == *other.p;
        }

        std::string as_math() const {
            return "¬" + p->as_math();
        }

        std::string as_sol() const {
            return "非<" + p->as_sol() + ">";
        }
    };

    std::variant<Primitive, Implication, Negation> const v;

    static Pro name(std::string s) {
        return std::make_shared<Prop const>(Primitive{s});
    }

    bool operator==(Prop const& other) const {
        if (v.index() != other.v.index()) {
            return false;
        }
        return std::visit([&](auto&& p) {
            return p == std::get<std::decay_t<decltype(p)>>(other.v);
        }, v);
    }

    friend Pro operator>=(Pro p, Pro q) {
        return std::make_shared<Prop const>(Implication{p, q});
    }

    friend Pro operator~(Pro p) {
        return std::make_shared<Prop const>(Negation{p});
    }

    std::string as_math() const {
        return std::visit([](auto&& p) {
            return p.as_math();
        }, v);
    }

    std::string as_sol() const {
        return std::visit([](auto&& p) {
            return p.as_sol();
        }, v);
    }
};

int num_known{0};

// 證 = proposition has been proven
struct Know {
    Pro const p;
    std::string const sol;
    int const id{num_known++};
};

// axiom schemas, see https://en.wikipedia.org/w/index.php?title=Hilbert_system&oldid=1225867602#Logical_axioms

// Ⅰ = `p → (q → p)`
Know A1(Pro p, Pro q) {
    auto ret = Know{
        p >= (q >= p),
        "Ⅰ<" + p->as_sol() + "," + q->as_sol() + ">"
    };
    std::cerr << ret.id << ". [A]\t\t" << ret.p->as_math() << "\n\n";
    return ret;
}

// Ⅱ = `(p → (q → r)) → ((p → q) → (p → r))`
Know A2(Pro p, Pro q, Pro r) {
    auto ret = Know{
        (p >= (q >= r)) >= ((p >= q) >= (p >= r)),
        "Ⅱ<" + p->as_sol() + "," + q->as_sol() + "," + r->as_sol() + ">"
    };
    std::cerr << ret.id << ". [B]\t\t" << ret.p->as_math() << "\n\n";
    return ret;
}

// Ⅲ = `(¬p → ¬q) → (q → p)`
Know A3(Pro p, Pro q) {
    auto ret = Know{
        (~p >= ~q) >= (q >= p),
        "Ⅲ<" + p->as_sol() + "," + q->as_sol() + ">"
    };
    std::cerr << ret.id << ". [C]\t\t" << ret.p->as_math() << "\n\n";
    return ret;
}

// 故 = modus ponens
Know MP(Know const& a, Know const& b) {
    auto& pq = std::get<Prop::Implication>(a.p->v);
    if (!(*pq.p == *b.p)) {
        throw std::logic_error{"Invalid modus ponens"};
    }
    auto ret = Know{
        pq.q,
        "故<" + a.sol + "," + b.sol + ">"
    };
    std::cerr << ret.id << ". [" << a.id << "," << b.id << "]\t" << ret.p->as_math() << "\n\n";
    return ret;
}

// the proof components are all linked from https://en.wikipedia.org/w/index.php?title=Hilbert_system&oldid=1225867602#Some_useful_theorems_and_their_proofs

// proves hypothetical syllogism metatheorem `p → q, q → r ⊢ p → r`, written by hand
// since proving the pure theorem is unnecessary https://en.wikipedia.org/w/index.php?title=Hypothetical_syllogism&oldid=1221253619#Proof_2
Know HS(Know const& pq, Know const& qr) {
    auto& a = std::get<Prop::Implication>(pq.p->v);
    auto p = a.p;
    auto q = a.q;
    auto r = std::get<Prop::Implication>(qr.p->v).q;
    auto l1 = A1(qr.p, p);
    auto l2 = MP(l1, qr);
    auto l3 = A2(p, q, r);
    return MP(MP(l3, l2), pq);
}

// proves `p → p`, following https://en.wikipedia.org/w/index.php?title=Propositional_calculus&oldid=1228311755#Example_of_a_proof_in_an_axiomatic_propositional_calculus_system
Know P1(Pro P) {
    auto k1 = A1(P, P >= P);
    auto k2 = A2(P, P >= P, P);
    auto k3 = MP(k2, k1);
    auto k4 = A1(P, P);
    auto k5 = MP(k3, k4);
    return k5;
}

// proves `p → ((p → q) → q)`, following https://en.wikipedia.org/w/index.php?title=Hilbert_system&oldid=1225867602#Some_useful_theorems_and_their_proofs
Know L2(Pro p, Pro q) {
    auto l1 = A2(p >= q, p, q);
    auto l2 = P1(p >= q);
    auto l3 = MP(l1, l2);
    auto l6 = A1(p, p >= q);
    auto l7 = HS(l6, l3);
    return l7;
}

// proves double negation theorem `¬¬p → p`, following https://en.wikipedia.org/w/index.php?title=Double_negation&oldid=1228947727#In_classical_propositional_calculus_system
Know DN(Pro p) {
    auto phi = p >= (p >= p);
    auto l1 = A1(p, p);
    auto l2 = A3(~phi, ~p);
    auto l3 = A3(p, phi);
    auto l4 = HS(l2, l3);
    auto l5 = A1(~~p, ~~phi);
    auto l6 = HS(l5, l4);
    auto l7 = L2(phi, p);
    auto l8 = MP(l7, l1);
    auto l9 = HS(l6, l8);
    return l9;
}

// 驗 checks the result
int main() {
    auto P = Prop::name("𝑝");
    auto fl = P1(P).sol;
    auto ag = DN(P).sol;
    std::cout << "驗<" << fl << ">𝑝𝑝;" << "驗<" << ag << ">𝑝;\n";
}
