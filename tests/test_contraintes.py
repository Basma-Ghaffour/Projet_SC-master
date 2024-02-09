import pytest
from Final.contraintes import (
    var_personnel,
    var_personnel_final,
    cost_1,
    cost_2,
    cost_3,
    cost_t,
    contr_final,
)


# test var_personnel


def test_var_personnel_val_error():
    with pytest.raises(ValueError):
        var_personnel(-10)


def test_var_personnel():
    assert var_personnel(0) == [0]
    assert var_personnel(2) == [0]
    assert var_personnel(3) == [-1, 0, 1]
    assert var_personnel(9) == list(range(-3, 4))
    assert var_personnel(6) == list(range(-2, 3))
    assert var_personnel(100) == list(range(-3, 4))


def test_var_personnel_sum():
    val_test = list(range(0, 11))
    for val in val_test:
        assert sum(var_personnel(val)) == 0


# test var_personnel_final

Liste = [("Janvier", 3), ("Fevrier", 0), ("Mars", 15)]


def test_var_personnel_final_val_error():
    with pytest.raises(ValueError):
        var_personnel_final(-2, Liste)


def test_var_personnel_final_contr_fin_non_respc():
    assert var_personnel_final(2, Liste) == "contrainte non respecter"


Liste2 = [("Janvier", 3), ("Fevrier", 0), ("Mars", 4)]


def test_var_personnel_final_contr_fin_respct():
    assert var_personnel_final(3, Liste2)


# test cost_1


def test_cost_1():
    assert cost_1(0) == 0
    assert cost_1(1) == 160
    assert cost_1(-1) == 160
    assert cost_1(2) == 320
    assert cost_1(-2) == 320


def test_cost_1_abs():
    val_test = list(range(-10, 11))
    for val in val_test:
        assert cost_1(val) == cost_1(-val)


# test cost_2


def test_cost_2_val_error():
    with pytest.raises(ValueError):
        cost_2(-1, 2)
    with pytest.raises(ValueError):
        cost_2(1, -2)
    with pytest.raises(ValueError):
        cost_2(-1, -2)


def test_cost_2_arg_egaux():
    val_test = [(x, x) for x in range(0, 11)]
    for val in val_test:
        assert cost_2(val[0], val[1]) == 0


def test_cost_2_no_contr():
    val_test = list(range(0, 11))
    for val in val_test:
        assert cost_2(val, 0) == 0


def test_cost_2_pers_sur_num():
    val_test = list(range(4, 11))
    for val in val_test:
        assert cost_2(val, 3) == 200 * (val - 3)


def test_cost_2_no_pers_sur_num():
    val_test = list(range(0, 6))
    for val in val_test:
        assert cost_2(val, 6) == 0


# test cost_3


def test_cost_3_val_error():
    with pytest.raises(ValueError):
        cost_3(-1, 2)
    with pytest.raises(ValueError):
        cost_3(1, -2)
    with pytest.raises(ValueError):
        cost_3(-1, -2)


def test_cost_3_no_pers_manq():
    val_test = list(range(4, 11))
    for val in val_test:
        assert cost_3(val, 3) == 0


def test_cost_3_arg_egaux():
    val_test = [(x, x) for x in range(0, 11)]
    for val in val_test:
        assert cost_3(val[0], val[1]) == 0


def test_cost_3_contr_non_resp():
    val_test_contr = list(range(0, 11))
    for val_c in val_test_contr:
        contr = val_c
        born_sup = contr * (100 / 125)
        val_test = list(range(0, int(born_sup)))
        for val in val_test:
            assert cost_3(val, contr) == "Contrainte non respecter"


def test_cost_3_pers_manq_contr_resp():
    val_test_contr = list(range(0, 11))
    for val_c in val_test_contr:
        contr = val_c
        born_inf = contr * (100 / 125)
        val_test = list(range(int(born_inf + 1), contr))
        for val in val_test:
            assert cost_3(val, contr) == 200 * int(contr - val)


# test cost_t


def test_cost_t_value_error():
    with pytest.raises(ValueError):
        cost_t(-1, 1, 1)
    with pytest.raises(ValueError):
        cost_t(-1, -1, 1)
    with pytest.raises(ValueError):
        cost_t(1, -1, 1)


def test_cost_t_no_contr():
    val_test = [
        (
            x,
            0,
            x,
        )
        for x in range(0, 11)
    ]
    for val in val_test:
        assert cost_t(val[0], val[1], val[2]) == cost_1(val[2])


def test_cost_t_cont_cont_3_non_respc():
    val_test_contr = list(range(0, 11))
    for val_c in val_test_contr:
        contr = val_c
        born_sup = contr * (100 / 125)
        val_test = list(range(0, int(born_sup)))
        for val in val_test:
            assert cost_t(val, contr, 10) == cost_3(val, contr)


def test_cost_t_contr_3_respc():
    val_test_contr = list(range(0, 11))
    for val_c in val_test_contr:
        contr = val_c
        born_inf = contr * (100 / 125)
        val_test = list(range(int(born_inf + 1), contr))
        for val in val_test:
            assert cost_t(val, contr, 2) == cost_1(2) + cost_2(val, contr) + cost_3(
                val, contr
            )


# test contr_final


def test_contr_final_contr_non_rspc():
    assert contr_final("Contrainte non respecter") == "contrainte non respecter"
    assert contr_final("") == "contrainte non respecter"


def test_contr_final_contr_rspc():
    assert contr_final(-1) == cost_1(-1)
