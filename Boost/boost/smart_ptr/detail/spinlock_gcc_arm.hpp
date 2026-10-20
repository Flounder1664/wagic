#ifndef BOOST_SMART_PTR_DETAIL_SPINLOCK_GCC_ARM_HPP_INCLUDED
#define BOOST_SMART_PTR_DETAIL_SPINLOCK_GCC_ARM_HPP_INCLUDED

//
//  Copyright (c) 2008 Peter Dimov
//
//  Distributed under the Boost Software License, Version 1.0.
//  See accompanying file LICENSE_1_0.txt or copy at
//  http://www.boost.org/LICENSE_1_0.txt)
//

#include <boost/smart_ptr/detail/yield_k.hpp>

namespace boost
{

namespace detail
{

class spinlock
{
public:

    int v_;

public:

    bool try_lock()
    {
        // Compiler builtin instead of hand-written asm: the old fallback used
        // 32-bit ARM "swp" (not an AArch64 instruction), which forced the build
        // onto -march=armv8.1-a + LSE and SIGILLed on pre-v8.1 cores.
        int r = __atomic_exchange_n( &v_, 1, __ATOMIC_ACQUIRE );
        return r == 0;
    }

    void lock()
    {
        for( unsigned k = 0; !try_lock(); ++k )
        {
            boost::detail::yield( k );
        }
    }

    void unlock()
    {
        __atomic_store_n( &v_, 0, __ATOMIC_RELEASE );
    }

public:

    class scoped_lock
    {
    private:

        spinlock & sp_;

        scoped_lock( scoped_lock const & );
        scoped_lock & operator=( scoped_lock const & );

    public:

        explicit scoped_lock( spinlock & sp ): sp_( sp )
        {
            sp.lock();
        }

        ~scoped_lock()
        {
            sp_.unlock();
        }
    };
};

} // namespace detail
} // namespace boost

#define BOOST_DETAIL_SPINLOCK_INIT {0}

#endif // #ifndef BOOST_SMART_PTR_DETAIL_SPINLOCK_GCC_ARM_HPP_INCLUDED
