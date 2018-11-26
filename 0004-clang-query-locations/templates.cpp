
#include <vector>

namespace NS 
{

template<typename T>
struct Templ
{

    template<typename U>
    struct Inner
    {

    };

};

}

NS::Templ<NS::Templ<int>::template Inner<bool>> templateType()
{
    return {};
}
