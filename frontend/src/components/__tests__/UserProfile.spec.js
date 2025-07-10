import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import UserProfile from '../UserProfile.vue';

describe('UserProfile.vue', () => {
  it('renders user profile container', async () => {
    const wrapper = mount(UserProfile, {
      global: {
        mocks: {
          $store: {
            state: {},
            dispatch: () => {},
          },
        },
      },
    });
    // Wait for any async rendering
    await wrapper.vm.$nextTick();
    expect(wrapper.find('.user-profile').exists()).toBe(true);
  });
});
