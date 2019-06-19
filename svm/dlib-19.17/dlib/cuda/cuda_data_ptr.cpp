// Copyright (C) 2017  Davis E. King (davis@dlib.net)
// License: Boost Software License   See LICENSE.txt for the full license.
#ifndef DLIB_DNN_CuDA_DATA_PTR_CPP_
#define DLIB_DNN_CuDA_DATA_PTR_CPP_

#ifdef DLIB_USE_CUDA

#include "cuda_data_ptr.h"
#include "cuda_utils.h"

namespace dlib
{
    namespace cuda 
    {

    // -----------------------------------------------------------------------------------

        cuda_data_void_ptr::
        cuda_data_void_ptr(
            size_t n
        ) : num(n)
        {
            if (n == 0)
                return;

            void* data = nullptr;

            CHECK_CUDA(cudaMalloc(&data, n));
            pdata.reset(data, [](void* ptr){
                auto err = cudaFree(ptr);
                if(err!=cudaSuccess)
                std::cerr << "cudaFree() failed. Reason: " << cudaGetErrorString(err) << std::endl;
            });
        }

    // ------------------------------------------------------------------------------------

        void memcpy(
            void* dest,
            const cuda_data_void_ptr& src,
            const size_t num
        )
        {
            DLIB_ASSERT(num <= src.size());
            if (src.size() != 0)
            {
                CHECK_CUDA(cudaMemcpy(dest, src.data(),  num, cudaMemcpyDefault));
            }
        }

    // ------------------------------------------------------------------------------------

        void memcpy(
            void* dest,
            const cuda_data_void_ptr& src
        )
        {
            memcpy(dest, src, src.size());
        }

    // ------------------------------------------------------------------------------------

        void memcpy(
            cuda_data_void_ptr dest, 
            const void* src,
            const size_t num
        )
        {
            DLIB_ASSERT(num <= dest.size());
            if (dest.size() != 0)
            {
                CHECK_CUDA(cudaMemcpy(dest.data(), src, num, cudaMemcpyDefault));
            }
        }

    // ------------------------------------------------------------------------------------

        void memcpy(
            cuda_data_void_ptr dest, 
            const void* src
        )
        {
            memcpy(dest,src,dest.size());
        }

    // ------------------------------------------------------------------------------------

        class cudnn_device_buffer
        {
        public:
            // not copyable
            cudnn_device_buffer(const cudnn_device_buffer&) = delete;
            cudnn_device_buffer& operator=(const cudnn_device_buffer&) = delete;

            cudnn_device_buffer()
            {
                buffers.resize(16);
            }
            ~cudnn_device_buffer()
            {
            }

            std::shared_ptr<resizable_cuda_buffer> get_buffer (
            )
            {
                int new_device_id;
                CHECK_CUDA(cudaGetDevice(&new_device_id));
                // make room for more devices if needed
                if (new_device_id >= (long)buffers.size())
                    buffers.resize(new_device_id+16);

                // If we don't have a buffer already for this device then make one
                std::shared_ptr<resizable_cuda_buffer> buff = buffers[new_device_id].lock();
                if (!buff)
                {
                    buff = std::make_shared<resizable_cuda_buffer>();
                    buffers[new_device_id] = buff;
                }

                // Finally, return the buffer for the current device
                return buff;
            }

        private:

            std::vector<std::weak_ptr<resizable_cuda_buffer>> buffers;
        };

        std::shared_ptr<resizable_cuda_buffer> device_global_buffer()
        {
            thread_local cudnn_device_buffer buffer;
            return buffer.get_buffer();
        }

    // ------------------------------------------------------------------------------------

    }  
}

#endif // DLIB_USE_CUDA

#endif // DLIB_DNN_CuDA_DATA_PTR_CPP_


