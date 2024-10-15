from django.test import TestCase

# Create your tests here.
new_pknown = round(0.2000,2)
print(new_pknown)
print(type(new_pknown))
print(type(0.3))


def testing(student_facts):
    facts = []

    for fact_str in student_facts:
        fact_args = fact_str.replace("Fact(", "").replace(")", "").strip()

        print(f"Processing fact: {fact_str}")

        args = {}
        for arg in fact_args.split(','):
            try:
                k, v = arg.split('=')
                k = k.strip()
                v = v.strip().strip("'")
                args[k] = v
                print(args)
            except ValueError as e:
                print(f"Error processing argument '{arg}': {e}")

        # fact = Fact(**args)
        # facts.append(fact)
        
testing(["Fact(concept='VAT', imported_services='Non')"])