from itertools import product

def gcd(x, y):
    """Calcule le PGCD de x et y avec gcd(0,0) = 0"""
    while y != 0:
        x, y = y, x % y
    return abs(x) if x != 0 else 0

def is_endomorphism(f, M):
    """Vérifie si f préserve l'opération de PGCD"""
    return all(f[gcd(x, y)] == gcd(f[x], f[y]) for x, y in product(M, repeat=2))

def is_idempotent(f, M):
    """Vérifie si f ∘ f = f"""
    return all(f[f[x]] == f[x] for x in M)

def direct_image(f, M):
    """Calcule l'image directe de f"""
    return {f[x] for x in M}

def extended_image(f, M):
    """Calcule l'image étendue sous PGCD"""
    im_f = direct_image(f, M)
    return {y for y in M if any(gcd(y, f[x]) in im_f for x in M)}

def kernel(f, M):
    """Calcule le noyau de f (valeurs où f(x) = 0)"""
    return {x for x in M if f[x] == 0}

def generate_valid_functions(M):
    """Génère tous les endomorphismes valides"""
    functions = []
    for f_vals in product(M, repeat=len(M)):
        f = dict(enumerate(f_vals))
        if f[0] == 0 and is_endomorphism(f, M):
            functions.append(f)
    return functions

def analyze_functions(M):
    """Affiche un tableau analysant les endomorphismes et vérifie si M est w-Rickart"""
    valid_functions = generate_valid_functions(M)
    idempotents = [g for g in valid_functions if is_idempotent(g, M)]

    # Affichage du tableau
    print("\nEndomorphisme".ljust(20), "Idempotent".ljust(15), "Noyau".ljust(20),
          "Image".ljust(20), "Image étendue".ljust(20), "i-régulier")
    print("-" * 110)

    for f in valid_functions:
        f_tuple = tuple(f[i] for i in sorted(M))
        im = direct_image(f, M)
        im_et = extended_image(f, M)
        ker = kernel(f, M)

        line = f"{str(f_tuple).ljust(18)} | "
        line += f"{'Oui'.ljust(13) if is_idempotent(f, M) else 'Non'.ljust(13)} | "
        line += f"{str(ker).ljust(18)} | "
        line += f"{str(im).ljust(18)} | "
        line += f"{str(im_et).ljust(18)} | "
        line += "Oui" if im == im_et else "Non"  # Vérification i-régulier
        print(line)

    # Vérification de la propriété w-Rickart
    is_w_Rickart = True
    for f in valid_functions:
        im_et_f = extended_image(f, M)
        if not any(im_et_f == kernel(g, M) for g in idempotents):
            is_w_Rickart = False
            break

    # Affichage du résultat final
    print("\nConclusion :")
    print("M est un semi-module w-Rickart :", "Oui" if is_w_Rickart else "Non")

# Exemple d'utilisation
n = 2  # Tu peux modifier la taille de l'ensemble
M = list(range(n + 1))
analyze_functions(M)
