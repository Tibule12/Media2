import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Logout from '../Logout.vue';
import { createStore } from 'vuex';
import { createRouter, createMemoryHistory } from 'vue-router';

describe('Logout.vue', () => {
  it('renders logout button', async () => {
    const store = createStore({
      actions: {
        logout: () => Promise.resolve(),
      },
    });
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [],
    });
    const wrapper = mount(Logout, {
      global: {
        plugins: [store, router],
      },
    });
    // Wait for mounted hook to complete
    await wrapper.vm.$nextTick();
    expect(wrapper.find('button').exists()).toBe(true);
  });
});
